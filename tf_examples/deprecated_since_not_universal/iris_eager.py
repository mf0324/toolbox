# coding: utf-8

"""
Iris鸢尾花分类问题
用eager来搞
"""

from __future__ import absolute_import, division, print_function

import os

# do not do plot. since we are in tty(ssh) of a server.
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow.contrib.eager as tfe  ##!! important

tf.enable_eager_execution()





def parse_csv(line):
    """
    解析数据，返回(features, label)元组
    """
    example_defaults = [[0.], [0.], [0.], [0.], [0]]  # 设定默认值
    parsed_line = tf.decode_csv(line, example_defaults)
    # 前四列是特征。整到一起。
    features = tf.reshape(parsed_line[:-1], shape=(4,))
    # 最后一列是label
    label = tf.reshape(parsed_line[-1], shape=())
    return features, label

def get_train_dataset():
    """
    download dataset and manipulate to standard input
    """
    train_dataset_url = 'http://download.tensorflow.org/data/iris_training.csv'
    train_dataset_fp = tf.keras.utils.get_file(
        fname=os.path.basename(train_dataset_url), origin=train_dataset_url
    )
    print('Local copy of the dataset file: {}'.format(train_dataset_fp))
    train_dataset = tf.data.TextLineDataset(train_dataset_fp)
    train_dataset = train_dataset.skip(1).map(parse_csv).shuffle(buffer_size=1000).batch(32)
    return train_dataset

    # Now we can access each batch of data via:
    #features, label = iter(train_dataset).next()
    #print('example features:', features[0])
    #print('exampole label:', label[0])

def get_test_dataset():
    """
    下载测试数据
    """
    test_url= 'http://download.tensorflow.org/data/iris_test.csv'
    test_fp = tf.keras.utils.get_file(fname=os.path.basename(test_url), origin=test_url)

    test_dataset = tf.data.TextLineDataset(test_fp)
    test_dataset = test_dataset.skip(1).map(parse_csv).shuffle(1000).batch(32)

    return test_dataset



def create_model():
    """
    创建模型
    3个全连接层。用keras了。anyway，能出活儿就是好东西
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(3)
    ])
    return model


def loss(model, x, y):
    """定义损失函数"""
    y_ = model(x)
    # y是gt label，y和y_的编码形式为一个整数，代表类别索引。所以，使用tf.losses.sparse_softmax_cross_entropy
    return tf.losses.sparse_softmax_cross_entropy(labels=y, logits=y_)

def grad(model, inputs, targets):
    """计算梯度。这个函数的细节不太懂。返回什么？输入什么？"""
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, model.variables)


def eager_run():
    ############
    #   train
    ############
    train_dataset = get_train_dataset()
    model = create_model()

    # 创建优化器
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

    # 记录每个epoch的loss,用于绘图。不用tensorboard嘛？
    train_loss_results = []
    train_accuracy_results = []

    num_epochs = 201
    for epoch in range(num_epochs):
        epoch_loss_avg = tfe.metrics.Mean()
        epoch_accuracy = tfe.metrics.Accuracy()

        # Training loop, batch size 32
        for x, y in train_dataset:
            # Optimize the model
            grads = grad(model, x, y)
            optimizer.apply_gradients(zip(grads, model.variables),
                                  global_step=tf.train.get_or_create_global_step())

            # Track progress
            epoch_loss_avg(loss(model, x, y))  # add current batch loss
            epoch_accuracy(tf.argmax(model(x), axis=1, output_type=tf.int32), y)

        # end epoch
        train_loss_results.append(epoch_loss_avg.result())
        train_accuracy_results.append(epoch_accuracy.result())

        if epoch % 50 == 0:
            print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                epoch_loss_avg.result(),
                                                                epoch_accuracy.result()))
    plot_training_loss(train_loss_results, train_accuracy_results)


    ##############
    #    eval
    ##############

    # 在测试集上evaluation
    test_dataset = get_test_dataset()

    test_accuracy = tfe.metrics.Accuracy()

    for (x, y) in test_dataset:
        prediction = tf.argmax(model(x), axis=1, output_type=tf.int32)
        test_accuracy(prediction, y)

    print('Test set accuracy: {:.3f}%'.format(test_accuracy.result()))


    ##############
    #  infer/test
    ##############
    # 使用训练好的模型预测
    class_ids = ["Iris setosa", "Iris versicolor", "Iris virginica"]

    predict_dataset = tf.convert_to_tensor([
        [5.1, 3.3, 1.7, 0.5,],
        [5.9, 3.0, 4.2, 1.5,],
        [6.9, 3.1, 5.4, 2.1]
    ])

    predictions = model(predict_dataset)

    for i, logits in enumerate(predictions):
        class_idx = tf.argmax(logits).numpy()
        name = class_ids[class_idx]
        print("Example {} prediction: {}".format(i, name))


def plot_training_loss(train_loss_results, train_accuracy_results):
    # 可视化损失函数vs.迭代次数变化趋势：用matplotlib
    fig, axes = plt.subplots(2, sharex=True, figsize=(12, 8))
    fig.suptitle('Training Metrics')

    axes[0].set_ylabel('Loss', fontsize=14)
    axes[0].plot(train_loss_results)

    axes[1].set_ylabel('Accuracy', fontsize=14)
    axes[1].set_xlabel('Epoch', fontsize=14)
    axes[1].plot(train_accuracy_results)

    plt.savefig('train_loss_accuracy_vs_iteration.png')



if __name__ == '__main__':
    eager_run()

# coding: utf-8

def frcnn_prepare_prototxt():
    """
    faster rcnn  loading prototxt and do modification on the fly. Then write to disk.

    准备prototxt，包括solver.pt里面名字的修改，以及train/val的prototxt中anchor数目、类别数目关联的地方
    如果每次实验都要完全手动改prototxt，真的太容易出错了。要根据指定的anchor数目、检测类别数等，来自动地生成prototxt

    对于solver.pt：
    检查solver.pt是否存在，如果不存在，则从models/std/$ARCH/$NET/solver.pt复制；
    检查solver.pt中net和snapshot的名字是和实验方案一致的

    对于train.pt和test.pt:
    确保anchor数、类别数相关的结果都正确
    """
    if os.path.exists(cfg.sv.path) is False:
        src_pth = osp.join(cfg.MODELS_ROOT, 'std', cfg.arch, cfg.net, 'solver.pt')
        dst_pth = osp.join(cfg.MODELS_ROOT, cfg.db, cfg.arch, cfg.net, cfg.lab, 'solver.pt')
        dst_pre = osp.split(dst_pth)[0]
        if os.path.exists(dst_pre) is False:
            os.makedirs(dst_pre)
        shutil.copyfile(src_pth, dst_pth)

    solver_param = caffe_pb2.SolverParameter()
    with open(cfg.sv.path, 'rt') as fin:
        pb2.text_format.Merge(fin.read(), solver_param)
    solver_param.train_net = "models/{db}/{arch}/{net}/{lab}/train.pt".format(db=cfg.db, arch=cfg.arch, net=cfg.net, lab=cfg.lab)
    solver_param.snapshot_prefix = "{db}_{arch}_{net}_{lab}".format(db=cfg.db, arch=cfg.arch, net=cfg.net, lab=cfg.lab)
    with open(cfg.sv.path, 'w') as fout:
        fout.write(str(solver_param))

    ## 首先检查train.pt和test.pt是否存在，不存在则从标准模板文件拷贝过去
    train_net_pth = solver_param.train_net
    if os.path.exists(train_net_pth) is False:
        src_pth = osp.join(cfg.MODELS_ROOT, 'std', cfg.arch, cfg.net, 'train.pt')
        print('src_pth is:', src_pth)
        print('train_net_pth is:', train_net_pth)
        shutil.copyfile(src_pth, train_net_pth)
    test_net_pth = train_net_pth.replace('train.pt', 'test.pt')
    if os.path.exists(test_net_pth) is False:
        src_pth = osp.join(cfg.MODELS_ROOT, 'std', cfg.arch, cfg.net, 'test.pt')
        shutil.copyfile(src_pth, test_net_pth)

    cfg.num_class = len(cfg.classes)
    cfg.num_anchor = len(cfg.ANCHORS.ratios) * len(cfg.ANCHORS.scales)
    ## 其次读取train.pt文件，确保其中的类别数、anchor数目正确
    train_net_param = caffe_pb2.NetParameter()
    with open(train_net_pth) as fin:
        pb2.text_format.Merge(fin.read(), train_net_param)
    layer_names = [_.name for _ in train_net_param.layer]
    ### rpn和frcnn的train.pt都需要修改的：
    num_class_str = "'num_classes': {:d}".format(cfg.num_class+1)  #这里冒号后面一定要有空格，不然protobuf无法解析而报错
    train_net_param.layer[layer_names.index('input-data')].python_param.param_str=num_class_str
    train_net_param.layer[layer_names.index('rpn_cls_score')].convolution_param.num_output = 2*cfg.num_anchor
    train_net_param.layer[layer_names.index('rpn_bbox_pred')].convolution_param.num_output = 4*cfg.num_anchor
    ### frcnn特有的
    if cfg.arch=='frcnn' or cfg.arch=='loco':
        train_net_param.layer[layer_names.index('roi-data')].python_param.param_str = num_class_str
        train_net_param.layer[layer_names.index('cls_score')].inner_product_param.num_output = cfg.num_class+1
        train_net_param.layer[layer_names.index('bbox_pred')].inner_product_param.num_output = 4*(cfg.num_class+1)
        train_net_param.layer[layer_names.index('rpn_cls_prob_reshape')].reshape_param.shape.dim[1] = 2*cfg.num_anchor
    with open(train_net_pth, 'w') as fout:
        fout.write(str(train_net_param))

    ## 对于test.pt文件，和train.pt类似，只不过字段不太一样
    test_net_param = caffe_pb2.NetParameter()
    with open(test_net_pth) as fin:
        pb2.text_format.Merge(fin.read(), test_net_param)
    layer_names = [_.name for _ in test_net_param.layer]
    test_net_param.layer[layer_names.index('rpn_cls_score')].convolution_param.num_output = 2*cfg.num_anchor
    test_net_param.layer[layer_names.index('rpn_bbox_pred')].convolution_param.num_output = 4*cfg.num_anchor
    test_net_param.layer[layer_names.index('rpn_cls_prob_reshape')].reshape_param.shape.dim[1] = 2*cfg.num_anchor
    if cfg.arch=='frcnn' or cfg.arch=='loco':
        test_net_param.layer[layer_names.index('cls_score')].inner_product_param.num_output = cfg.num_class+1
        test_net_param.layer[layer_names.index('bbox_pred')].inner_product_param.num_output = 4*(cfg.num_class+1)
    with open(test_net_pth, 'w') as fout:
        fout.write(str(test_net_param))


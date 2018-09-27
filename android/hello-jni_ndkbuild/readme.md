## Why this blog
现在（2018年9月27日），Android Studio中新建ndk项目都使用cmake而不是Android.mk+Application.mk的方式。但老项目需要维护，android.mk方式还需要过一遍。

本文在最新Android Studio中配置了`https://github.com/googlesamples/android-ndk/tree/android-mk/hello-jni`，并更新了gradle相应的配置。

## Get started
```
cd d:/work
git clone https://github.com/googlesamples/android-ndk
cd android-ndk
git checkout -b master-ndkbuild
```
拷贝hello-jni目录到`d:/work/AndroidProjects/hello-jni_ndkbuild`目录

用AS打开这个目录。发现是gradle构建的，但是新版AS有问题。

### 4.1 修改Project的`build.gradle`
原来的：
```groovy
// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    repositories {
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:2.3.0'
    }
}

allprojects {
    repositories {
        jcenter()
    }
}
```

改成：
```groovy
// Top-level build file where you can add configuration options common to all sub-projects/modules.
buildscript {
    repositories {
        jcenter()
        google() //新增
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.1.3' //修改版本。注意，这个版本和gradle-wrapper.properties中的gradle版本不是一回事。
    }
}

allprojects {
    repositories {
        jcenter()
    }
}

// 新增
task clean(type: Delete) {
    delete rootProject.buildDir
}
```

**大坑**
Project的`build.gradle`中的`com.android.tools.build:gradle:3.1.3`这个版本3.1.3，
和`gradle-wrapper.properties`中的gradle版本不是一回事。

### 4.2 修改gradle-wrapper.properties中的gradle版本
原来：
```
distributionUrl=https\://services.gradle.org/distributions/gradle-3.3-all.zip
```
新的：
```
distributionUrl=https\://services.gradle.org/distributions/gradle-4.4-all.zip
```

### 4.3 去掉app的`build.gradle`中的`buildToolsVersion`
新版gradle中，这个buildToolsVersion有副作用。扔掉。

### 4.4 gradle sync；build

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Euclid30K 数据集样本展示
========================

这个脚本展示Euclid30K数据集中的样本数据，包括问题、答案和图像。
"""

import pandas as pd
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64


def main():
    """主函数"""
    print("=" * 50)
    print("Euclid30K 数据集样本展示")
    print("=" * 50)
    
    # 设置数据集路径
    DATA_PATH = "/Users/jia/datasets/Euclid30K"
    
    # 加载数据集
    train_file = os.path.join(DATA_PATH, "Euclid30K_train.parquet")
    val_file = os.path.join(DATA_PATH, "Euclid30K_val.parquet")
    
    print("正在加载数据集...")
    train_df = pd.read_parquet(train_file)
    val_df = pd.read_parquet(val_file)
    
    print(f"训练集形状: {train_df.shape}")
    print(f"验证集形状: {val_df.shape}")
    print()
    
    # 显示列信息
    print("数据集列名:")
    for i, col in enumerate(train_df.columns):
        print(f"  {i+1}. {col}")
    print()
    
    # 显示训练集样本
    print("训练集样本:")
    for i in range(min(3, len(train_df))):
        print(f"\n样本 {i+1}:")
        display_sample(train_df.iloc[i], "训练集")
    
    print("\n" + "="*50)
    
    # 显示验证集样本
    print("验证集样本:")
    for i in range(min(3, len(val_df))):
        print(f"\n样本 {i+1}:")
        display_sample(val_df.iloc[i], "验证集")


def display_sample(row, dataset_type):
    """显示单个样本的所有信息"""
    # 显示问题和答案
    print(f"  问题: {row['problem']}")
    print(f"  答案: {row['answer']}")
    
    # 处理图像数据
    if 'images' in row and row['images'] is not None:
        image_data = row['images']
        print(f"  图像数据类型: {type(image_data)}")
        
        # 尝试解析图像
        try:
            if isinstance(image_data, np.ndarray) and len(image_data) > 0:
                # 处理numpy数组形式的图像数据
                first_img = image_data[0]
                if isinstance(first_img, dict):
                    show_image_from_dict(first_img, f"{dataset_type}_sample_{row.name}")
                else:
                    print(f"    图像数据格式未知: {type(first_img)}")
            elif isinstance(image_data, list) and len(image_data) > 0:
                # 处理列表形式的图像数据
                first_img = image_data[0]
                if isinstance(first_img, dict):
                    show_image_from_dict(first_img, f"{dataset_type}_sample_{row.name}")
                else:
                    print(f"    图像数据格式未知: {type(first_img)}")
            elif isinstance(image_data, dict):
                # 直接是字典形式的图像数据
                show_image_from_dict(image_data, f"{dataset_type}_sample_{row.name}")
            else:
                print(f"    无法处理的图像数据类型: {type(image_data)}")
        except Exception as e:
            print(f"    处理图像时出错: {e}")
    else:
        print("  无图像数据")


def show_image_from_dict(image_dict, filename):
    """从字典中显示图像"""
    if 'bytes' in image_dict and 'path' in image_dict:
        try:
            # 获取图像字节数据
            image_bytes = image_dict['bytes']
            
            # 如果是base64编码的字符串，则解码
            if isinstance(image_bytes, str):
                image_data = base64.b64decode(image_bytes)
            else:
                image_data = image_bytes
            
            # 保存图像到文件
            with open(f'{filename}.jpg', 'wb') as f:
                f.write(image_data)
            
            print(f"    图像已保存为: {filename}.jpg")
            print(f"    图像路径: {image_dict['path']}")
        except Exception as e:
            print(f"    保存图像时出错: {e}")
    else:
        print(f"    图像字典结构不完整: {list(image_dict.keys()) if isinstance(image_dict, dict) else 'Not a dict'}")


if __name__ == "__main__":
    main()
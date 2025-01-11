import os
import pandas as pd
import streamlit as st
import pyperclip  # 用于复制文本

# 设置输出目录
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Streamlit 页面标题
st.sidebar.title("Words2mp3")

# 读取 Excel 文件
def read_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()  # 去除列名空格
        return df
    except Exception as e:
        st.error(f"读取 Excel 文件时出错: {e}")
        return None

# 读取 list.xlsx 文件并显示组内容
def display_group_content(file_path, selected_groups):
    df = read_excel(file_path)
    if df is not None:
        # 获取每个组及对应的单词和解释
        groups = df.groupby(df.columns[0])
        for group_name, group_data in groups:
            if group_name in selected_groups:
                st.subheader(f"组名: {group_name}")
                content = ""
                for _, row in group_data.iterrows():
                    word = row[2]  # 单词在第三列
                    explanation = row[3]  # 解释在第四列
                    content += f"单词: {word}\n解释: {explanation}\n\n"
                    st.markdown(f"<h2>{word}</h2>", unsafe_allow_html=True)  # 显示单词
                    st.markdown(f"<p>{explanation}</p><hr>", unsafe_allow_html=True)  # 显示解释
                
                # 添加复制按钮
                copy_button = st.button(f"复制 {group_name} 内容")
                if copy_button:
                    pyperclip.copy(content)  # 将内容复制到剪贴板
                    st.success(f"已复制 {group_name} 内容!")

# 读取 Excel 文件并显示组列表
def display_group_list(file_path):
    df = read_excel(file_path)
    if df is not None:
        groups = df.groupby(df.columns[0]).groups.keys()
        return list(groups)
    return []

# 开始处理 Excel 文件
if __name__ == "__main__":
    file_path = "list.xlsx"
    
    # 显示组选择
    available_groups = display_group_list(file_path)
    select_all = st.sidebar.checkbox("全选", value=False)  # 添加全选复选框
    if select_all:
        selected_groups = available_groups  # 如果全选勾选，选择所有组
    else:
        selected_groups = st.sidebar.multiselect("选择组", available_groups)  # 多选框供用户选择
    
    # 显示组选择的按钮
    if selected_groups:
        if st.button("显示选择的组"):
            with st.spinner("加载中..."):
                # 显示每个选择的组内容
                display_group_content(file_path, selected_groups)
    else:
        st.warning("请选择组以显示内容。")

# 侧边栏底部反馈信息
st.sidebar.markdown("---")
st.sidebar.write("<h2> 使用说明</h2><p>选择组后，可以点击显示每个组的内容，并复制到剪贴板。</p><p>Made by：川哥</p>", unsafe_allow_html=True)

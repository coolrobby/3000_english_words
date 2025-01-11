import streamlit as st
import pandas as pd

# 加载Excel文件
file_path = 'list.xlsx'  # 假设文件在当前文件夹中
df = pd.read_excel(file_path)

# 创建一个字典来保存按第一列分组的数据
grouped = df.groupby(df.columns[0])

# 创建侧边栏，显示100个任务超链接
tasks = [f"Task{i+1}" for i in range(100)]
task_dict = {task: idx for idx, task in enumerate(tasks)}

# 在侧边栏显示超链接
st.sidebar.title('Navigation')
selected_task = st.sidebar.radio('Choose a Task', tasks)

# 获取选择的任务对应的数据
task_idx = task_dict[selected_task]
group_name = df.iloc[task_idx, 0]  # 获取对应组的名称
group_data = grouped.get_group(group_name)

# 显示对应组的内容
st.title(f"Group: {group_name}")
for index, row in group_data.iterrows():
    st.markdown(f"### {row[2]}")  # 第三列内容，作为<h2>
    st.markdown(f"{row[3]}")      # 第四列内容，作为<p></p><hr>


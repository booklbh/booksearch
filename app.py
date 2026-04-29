import streamlit as st
import pandas as pd
import math

# --- 页面配置 ---
st.set_page_config(page_title="大数据量查询工具", layout="wide")

# --- 数据加载缓存 ---
@st.cache_data(show_spinner="正在加载 64 万行数据，请稍候...")
def load_data():
    # 假设你的文件名为 data.parquet
    df = pd.read_parquet("data.parquet")
    # 强制转换类型以节省内存
    df["名称"] = df["名称"].astype(str)
    df["索引文本"] = df["索引文本"].astype(str)
    return df

# 加载数据
try:
    df = load_data()
except FileNotFoundError:
    st.error("未找到 data.parquet 文件，请检查路径。")
    st.stop()

# --- 侧边栏：查询设置 ---
st.sidebar.header("查询筛选")
search_term = st.sidebar.text_input("输入名称进行模糊搜索", placeholder="例如：关键词...")

# --- 数据过滤逻辑 ---
if search_term:
    # 使用 str.contains 实现模糊搜索，case=False 不区分大小写
    filtered_df = df[df["名称"].str.contains(search_term, case=False, na=False)]
else:
    filtered_df = df

total_rows = len(filtered_df)

# --- 分页逻辑 ---
st.sidebar.markdown("---")
page_size = st.sidebar.number_input("每页显示行数", min_value=10, max_value=100, value=20)
total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
current_page = st.sidebar.number_input("当前页码", min_value=1, max_value=total_pages, value=1)

# 计算切片索引
start_idx = (current_page - 1) * page_size
end_idx = start_idx + page_size

# --- 主界面展示 ---
st.title("🔍 数据在线查询系统")
st.caption(f"当前数据总量：{len(df)} 行 | 搜索结果：{total_rows} 行")

if total_rows > 0:
    # 仅展示当前页的数据，避免浏览器渲染卡顿
    display_df = filtered_df.iloc[start_idx:end_idx]
    
    # 使用 Streamlit 高性能表格组件
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # 底部页码提示
    st.write(f"第 {current_page} / {total_pages} 页")
else:
    st.warning("没有找到匹配的结果，请更换关键词尝试。")

# --- 页脚 ---
st.markdown("---")
st.markdown("Built with Streamlit • 免费高效的数据查询方案")
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import json

EVALUATION_DATA = json.load(open(r"output/evaluation_results_umag.json", "r"))[
    "results"
]

# --- 2. 面板布局 ---

# 设置页面标题和布局
st.set_page_config(page_title="Retriever Evaluation Dashboard", layout="wide")

st.title("Retriever Performance Evaluation Dashboard")
st.markdown("---")

# --- 顶部区域：计算并显示平均指标分数 ---
if EVALUATION_DATA:
    # 提取所有分数
    scores_df = pd.DataFrame([item["scores"] for item in EVALUATION_DATA])

    # 计算平均值
    avg_recall_5 = scores_df["recall_at_5"].mean()
    avg_recall_20 = scores_df["recall_at_20"].mean()

    # 使用列布局居中显示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="**Recall@5**", value=f"{avg_recall_5:.2%}")
    with col2:
        st.metric(label="**Recall@20**", value=f"{avg_recall_20:.2%}")
    # with col3:
    #     st.metric(label="**Precision**", value=f"{avg_precision:.2%}")
else:
    st.warning("No evaluation data found.")

st.markdown("---")


# --- 侧边栏：问题列表和搜索 ---
st.sidebar.header("Questions")
search_query = st.sidebar.text_input("Search questions", "")

# 在侧边栏添加 Top-K 选择器
k_selection = st.sidebar.radio(
    "Display Top-K Retrieved Documents:",
    [5, 20],
    format_func=lambda x: f"Top {x}",  # 显示为 "Top 5", "Top 20"
)


if EVALUATION_DATA:
    # 根据搜索词过滤问题
    filtered_questions = [
        item["question"]
        for item in EVALUATION_DATA
        if search_query.lower() in item["question"].lower()
    ]

    if not filtered_questions:
        st.sidebar.warning("No questions match your search.")
        st.stop()  # 如果没有匹配项，停止执行以避免错误

    # 使用单选按钮来选择问题，点击后会自动刷新主区域
    selected_question = st.sidebar.radio(
        "Select a question to view details:", filtered_questions
    )

    # 查找选中问题对应的完整数据
    selected_item = next(
        (item for item in EVALUATION_DATA if item["question"] == selected_question),
        None,
    )

else:
    st.sidebar.info("No data to display.")
    selected_item = None


# --- 右侧主区域：显示选中问题的详细信息 ---
if selected_item:
    # 1. Question 板块
    st.header("Question")
    st.markdown(f"#### {selected_item['question']}")
    st.markdown("---")

    # 使用列布局并排显示 References 和 Retrieved
    col_ref, col_ret = st.columns(2, gap="large")

    with col_ref:
        # 2. Reference 板块
        st.subheader("Reference Documents")
        if selected_item["references"]:
            for i, doc in enumerate(selected_item["references"]):
                st.info(f"**Reference {i+1}:**\n\n{doc}")
        else:
            st.warning("No reference documents provided.")

    with col_ret:
        # 3. Retrieved 板块
        st.subheader(f"Retrieved Documents (Top {k_selection})")

        # 根据用户的选择来切片要显示的文档列表
        retrieved_to_display = selected_item["retrieved_context"][:k_selection]

        if retrieved_to_display:
            for i, doc in enumerate(retrieved_to_display):
                # 检查当前检索的文档是否在参考文档中，以高亮显示
                is_correct = doc in selected_item["references"]
                if is_correct:
                    st.success(f"**Retrieved {i+1}**\n\n{doc}")
                else:
                    st.error(f"**Retrieved {i+1}**\n\n{doc}")
        else:
            st.warning("No documents were retrieved.")

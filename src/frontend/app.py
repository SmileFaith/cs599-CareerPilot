import streamlit as st
import requests
import tempfile
import os
import sys

# Ensure src modules can be accessed if running from subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.tools.resume_reader import ResumeReaderTool

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="CareerPilot - AI求职成长助手", page_icon="🚀", layout="wide")

st.title("CareerPilot - AI求职成长助手 🚀")
st.write("欢迎使用基于多智能体的求职成长辅助系统。请按照下方标签页顺序进行操作。")

# Session state initialization
if "resume_info" not in st.session_state:
    st.session_state.resume_info = None
if "job_info" not in st.session_state:
    st.session_state.job_info = None
if "gap_report" not in st.session_state:
    st.session_state.gap_report = None
if "learning_plan" not in st.session_state:
    st.session_state.learning_plan = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None

tab1, tab2, tab3, tab4, tab5 = st.tabs(["1. 上传简历", "2. 输入岗位", "3. 差距报告", "4. 学习路线", "5. 面试模拟"])

with tab1:
    st.header("📄 第一步：上传简历解析")
    uploaded_file = st.file_uploader("支持上传 PDF 或 DOCX 格式的简历", type=["pdf", "docx"])

    if uploaded_file and st.button("开始解析简历"):
        # Save uploaded file to temp file to reuse ResumeReaderTool
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            with st.spinner("正在提取简历内容..."):
                text = ResumeReaderTool.read_file(tmp_path)

            with st.spinner("AI 正在解析简历信息..."):
                response = requests.post(f"{API_BASE_URL}/analyze-resume", json={"text": text})
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data["success"]:
                        st.session_state.resume_info = res_data["data"]
                        st.success("简历解析成功！")
                        st.json(st.session_state.resume_info)
                    else:
                        st.error(f"AI解析失败: {res_data['message']}")
                else:
                    st.error("API服务异常，请确认FastAPI后台是否已启动。")
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

with tab2:
    st.header("🎯 第二步：输入目标岗位 (JD)")
    jd_text = st.text_area("请将职位描述（JD文本）粘贴到下方", height=200)

    if jd_text and st.button("开始分析岗位"):
        with st.spinner("AI 正在提取岗位核心要求..."):
            try:
                response = requests.post(f"{API_BASE_URL}/analyze-job", json={"description": jd_text})
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data["success"]:
                        st.session_state.job_info = res_data["data"]
                        st.success("岗位分析成功！")
                        st.json(st.session_state.job_info)
                    else:
                        st.error(f"分析失败: {res_data['message']}")
                else:
                    st.error("API服务异常，请确认FastAPI后台是否已启动。")
            except Exception as e:
                st.error(f"请求服务发生错误: {str(e)}")

with tab3:
    st.header("📊 第三步：能力匹配度报告")
    if st.session_state.resume_info and st.session_state.job_info:
        if st.button("生成匹配度与差距报告"):
            with st.spinner("AI 正在比对各项能力指标..."):
                try:
                    payload = {
                        "resume_info": st.session_state.resume_info,
                        "job_info": st.session_state.job_info
                    }
                    response = requests.post(f"{API_BASE_URL}/gap-analysis", json=payload)
                    if response.status_code == 200:
                        res_data = response.json()
                        if res_data["success"]:
                            st.session_state.gap_report = res_data["data"]
                            st.success("报告生成完成！")

                            score = st.session_state.gap_report.get("score", 0)
                            st.metric(label="能力综合匹配度评分", value=f"{score} / 100")

                            col1, col2 = st.columns(2)
                            with col1:
                                st.subheader("✅ 已具备的优势技能")
                                for s in st.session_state.gap_report.get("matched_skills", []):
                                    st.markdown(f"- **{s}**")

                            with col2:
                                st.subheader("❌ 待提升的缺失技能")
                                for s in st.session_state.gap_report.get("missing_skills", []):
                                    st.markdown(f"- **{s}**")
                        else:
                            st.error(f"分析失败: {res_data['message']}")
                except Exception as e:
                    st.error(f"请求服务发生错误: {str(e)}")

        # Display existing report if previously calculated
        elif st.session_state.gap_report:
            score = st.session_state.gap_report.get("score", 0)
            st.metric(label="能力综合匹配度评分", value=f"{score} / 100")
            # ... UI element regeneration skipped for brevity outside the button click
    else:
        st.info("💡 请先完成「简历解析」和「岗位分析」，方可生成评估报告。")

with tab4:
    st.header("🗺️ 第四步：定制学习路线")
    if st.session_state.gap_report:
        if st.button("生成个性化学习路线"):
            with st.spinner("AI 正在排期学习路径..."):
                try:
                    payload = {
                        "gap_report": st.session_state.gap_report
                    }
                    response = requests.post(f"{API_BASE_URL}/learning-plan", json=payload)
                    if response.status_code == 200:
                        res_data = response.json()
                        if res_data["success"]:
                            st.session_state.learning_plan = res_data["data"]
                            st.success("学习路线生成成功！")
                        else:
                            st.error(f"生成失败: {res_data['message']}")
                except Exception as e:
                    st.error(f"请求服务发生错误: {str(e)}")

        if st.session_state.learning_plan:
            plan = st.session_state.learning_plan

            st.subheader("📌 推荐学习顺序")
            st.info(" → ".join(plan.get("learning_sequence", [])))

            st.subheader("📅 双周/月度排期")
            for week, tasks in plan.get("weekly_roadmap", {}).items():
                st.markdown(f"#### **{week.capitalize()}**")
                for t in tasks:
                    st.write(f"- {t}")

            st.subheader("💡 练手项目推荐")
            for p in plan.get("recommended_projects", []):
                st.write(f"- 🚀 {p}")
    else:
        st.info("💡 请先完成「差距报告」的生成，以帮助AI确位你的薄弱项。")

with tab5:
    st.header("🎙️ 第五步：AI 面试模拟")
    if st.session_state.job_info:
        if st.button("根据 JD 生成专属面试题"):
            with st.spinner("AI 考官正在出题..."):
                try:
                    payload = {"job_info": st.session_state.job_info}
                    response = requests.post(f"{API_BASE_URL}/interview", json=payload)
                    if response.status_code == 200:
                        res_data = response.json()
                        if res_data["success"]:
                            st.session_state.interview_questions = res_data["data"]
                            st.success("面试题目准备就绪！")
                        else:
                            st.error(f"生成失败: {res_data['message']}")
                except Exception as e:
                    st.error(f"请求服务发生错误: {str(e)}")

        if st.session_state.interview_questions:
            qs = st.session_state.interview_questions
            col_t, col_b = st.columns(2)

            with col_t:
                st.subheader("💻 技术深度问答")
                for i, q in enumerate(qs.get("technical_questions", []), 1):
                    st.write(f"**Q{i}:** {q}")

            with col_b:
                st.subheader("🤝 综合行为考察")
                for i, q in enumerate(qs.get("behavioral_questions", []), 1):
                    st.write(f"**Q{i}:** {q}")
    else:
        st.info("💡 请先完成「岗位分析」，AI考官网可基于JD出题。")


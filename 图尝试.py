import streamlit as st
import numpy as np

# 设置页面配置
st.set_page_config(page_title="CDUT 渣土泥浆智能智配系统", layout="centered")


# --- 模拟底层模型算法 ---
def predict_ucs(dosage, water_content, plasticity_index):
    # 模拟补偿算法逻辑：基础强度 = 0.82 * 掺量 + 0.96 (参考你的CDUT 2代拟合公式)
    # 加入渣土性质调节因子 (含水率和塑性指数会负向影响强度)
    adjustment = (40 - water_content) * 0.05 + (25 - plasticity_index) * 0.02
    base_strength = 0.82 * dosage + 0.96
    predicted_strength = base_strength + adjustment
    return max(predicted_strength, 0.1)


# --- UI 界面设计 ---
st.title("🏗️ CDUT 渣土泥浆智能智配系统")
st.markdown("---")

# 第一部分：输入端
st.subheader("1. 输入渣土基础指标")
col1, col2 = st.columns(2)
with col1:
    w = st.number_input("初始含水率 W (%)", value=45.0, step=0.1)
    ip = st.number_input("塑性指数 Ip", value=22.0, step=0.1)
with col2:
    f = st.number_input("细颗粒含量 (%)", value=75.0, step=0.1)
    dosage = st.slider("预设固化剂掺量 (%)", 7.0, 15.0, 10.0)

# 第二部分：智能计算
if st.button("开始秒级生成配比方案"):
    strength = predict_ucs(dosage, w, ip)
    error_range = strength * 0.08  # 预测精度误差控制在8%以内

    st.success("✅ 配比方案生成完毕！")

    # 第三部分：结果展示
    st.subheader("2. 强度预测结果")
    c1, c2 = st.columns(2)
    c1.metric("预估 28d UCS 强度", f"{strength:.2f} MPa")
    c2.metric("预测误差范围", f"±{error_range:.2f} MPa")

    # 第四部分：资源化建议定向
    st.subheader("3. 资源化处置建议")
    if strength >= 10.0:
        st.info("💡 建议方向：**标准路基材料 / 建筑保温砖材**")
        st.write("产品可作为高价值建材利用，满足高标基建需求。")
    elif strength >= 2.0:
        st.info("💡 建议方向：**工程回填材料 / 施工辅助材料**")
        st.write("满足流态固化土回填标准，实现渣土原位消纳。")
    else:
        st.warning("⚠️ 建议方向：**低要求场地平整 / 矿坑修复**")
        st.write("强度较低，建议增加 CDUT 固化剂掺量或复配激发剂。")

    # 第五部分：低碳评估 [cite: 3]
    st.subheader("4. 环境效益评估")
    reduction = 72.4  # 相比传统方案降幅达 72.4% [cite: 3]
    st.write(f"☘️ 采用本方案，相较于传统水泥外运填埋，碳排放预计降低 **{reduction}%**。")

# 侧边栏说明
st.sidebar.title("技术支撑")
st.sidebar.info("""
- **模型库**：500+组实验数据 
- **核心材料**：CDUT 复合固化剂 [cite: 1]
- **预测精度**：R² 分布在 0.88-0.93 之间 
""")
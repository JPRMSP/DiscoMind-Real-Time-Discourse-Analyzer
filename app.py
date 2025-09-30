import streamlit as st
import re
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧠 DiscoMind - Discourse Analyzer", layout="wide")

st.title("🧠 DiscoMind: Real-Time Discourse Analyzer")
st.markdown("""
Analyze any text using **Western Discourse Analysis** and **Mimamsa Principles** — with real-time visualization 🌐  
No pre-trained models. No datasets. 100% custom NLP logic.
""")

# --- Input Text ---
text = st.text_area("📜 Paste your text or discourse:", height=200,
                    placeholder="Enter any paragraph, article, or Vedic sentence here...")

if st.button("🔍 Analyze"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        # ---------- 1️⃣ TEXT SEGMENTATION ----------
        st.subheader("1️⃣ Text Segmentation (Western Perspective)")
        segments = [seg.strip() for seg in re.split(r'[.!?]', text) if seg.strip()]
        for i, seg in enumerate(segments, 1):
            st.write(f"**Segment {i}:** {seg}")

        # ---------- 2️⃣ LEXICAL CHAINS ----------
        st.subheader("2️⃣ Lexical Chains & Cohesion")
        words = re.findall(r'\b\w+\b', text.lower())
        freq = Counter(words)
        lexical_chain = [w for w, c in freq.items() if c > 1 and len(w) > 3]
        st.write("🔗 **Lexical Chains:**", ", ".join(lexical_chain) if lexical_chain else "No strong chains found.")

        # ---------- 3️⃣ INTENT & RHETORICAL STRUCTURE ----------
        st.subheader("3️⃣ Intent & Rhetorical Structure")
        intents = []
        for seg in segments:
            seg_lower = seg.lower()
            if any(w in seg_lower for w in ["because", "since", "therefore"]):
                intents.append("Cause-Effect")
            elif any(w in seg_lower for w in ["however", "but", "although"]):
                intents.append("Contrast")
            elif any(w in seg_lower for w in ["for example", "such as"]):
                intents.append("Elaboration")
            else:
                intents.append("Statement")
        for i, intent in enumerate(intents, 1):
            st.write(f"**Segment {i} Intent:** {intent}")

        # ---------- 4️⃣ MIMAMSA CLASSIFICATION ----------
        st.subheader("4️⃣ Mimamsa Sentence Classification")
        classifications = []
        for seg in segments:
            seg_lower = seg.lower()
            if any(w in seg_lower for w in ["must", "should", "shall"]):
                classifications.append("Obligatory Statement")
            elif any(w in seg_lower for w in ["may", "can"]):
                classifications.append("Non-Obligatory Statement")
            else:
                classifications.append("Procedural or Descriptive")
        for i, cls in enumerate(classifications, 1):
            st.write(f"**Segment {i} Mimamsa Type:** {cls}")

        # ---------- 5️⃣ SENTENCE REQUIREMENT CHECKS ----------
        st.subheader("5️⃣ Sentence Requirement Checks (Akanksha, Sannidhi, Yogyata)")
        akanksha = "✅ Satisfied" if len(words) > 5 else "⚠️ Possibly Unsatisfied"
        sannidhi = "✅ Contextually Connected" if len(segments) > 1 else "⚠️ Weak Connection"
        yogyata = "✅ Semantically Compatible" if len(lexical_chain) > 0 else "⚠️ Limited Cohesion"

        st.write(f"**Akanksha (Expectation):** {akanksha}")
        st.write(f"**Sannidhi (Proximity):** {sannidhi}")
        st.write(f"**Yogyata (Compatibility):** {yogyata}")

        # ---------- 6️⃣ SIX TESTS OF SUBSIDIARY ----------
        st.subheader("6️⃣ Six Mimamsa Tests of a Subsidiary")
        tests = {
            "Sruthi": "📜 Direct scriptural statement detected." if "veda" in text.lower() else "❌ No direct scriptural element.",
            "Linga": "📍 Indicative intention markers found." if any(w in text.lower() for w in ["thus", "therefore"]) else "❌ No strong indicators.",
            "Vakya": "✅ Syntactically complete sentences present." if len(segments) > 0 else "❌ Incomplete discourse.",
            "Prakarna": "✅ Context inferred from multiple sentences." if len(segments) > 1 else "❌ Limited context.",
            "Sthana": "✅ Order and sequence maintained." if text == " ".join(text.split()) else "⚠️ Formatting issues.",
            "Samakhya": "✅ Consistent naming terms found." if len(lexical_chain) > 0 else "❌ No repetition detected."
        }
        for k, v in tests.items():
            st.write(f"**{k}:** {v}")

        st.success("✅ Discourse Analysis Completed!")

        # ---------- 📊 VISUALIZATION 1: DISCOURSE TREE ----------
        st.subheader("🌳 Discourse Tree Visualization")
        G = nx.DiGraph()
        G.add_node("Discourse")
        for i, seg in enumerate(segments, 1):
            G.add_node(f"S{i}: {intents[i-1]}")
            G.add_edge("Discourse", f"S{i}: {intents[i-1]}")

        fig, ax = plt.subplots(figsize=(10, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2500, font_size=9, font_weight="bold", ax=ax)
        st.pyplot(fig)

        # ---------- 📈 VISUALIZATION 2: LEXICAL COHESION NETWORK ----------
        if lexical_chain:
            st.subheader("🔗 Lexical Cohesion Network")
            G2 = nx.Graph()
            for w in lexical_chain:
                G2.add_node(w)
            for i in range(len(lexical_chain)):
                for j in range(i + 1, len(lexical_chain)):
                    G2.add_edge(lexical_chain[i], lexical_chain[j])

            fig2, ax2 = plt.subplots(figsize=(8, 6))
            pos2 = nx.spring_layout(G2, seed=42)
            nx.draw(G2, pos2, with_labels=True, node_color="lightgreen", node_size=2000, font_size=10, font_weight="bold", ax=ax2)
            st.pyplot(fig2)
        else:
            st.info("No significant lexical cohesion network to display.")

st.markdown("---")
st.markdown("💡 *Developed as a fusion of Western Discourse Analysis & Eastern Mimamsa Logic*")

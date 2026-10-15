import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.title("Skills Hub")
st.caption("[Source on GitHub](https://github.com/mdeleon6/ai-data-skills-hub)")


df = pd.read_csv("skills.csv")

# Across both tracks: one row per track
st.subheader("Overview")
summary = df.groupby("track")[["level", "target"]].mean().round(1)
st.dataframe(summary)

# One track at a time
track = st.radio("Track", df["track"].unique(), horizontal=True)
view = df[df["track"] == track]

c1, c2, c3 = st.columns(3)
c1.metric("Average level", f"{view['level'].mean():.1f}")
c2.metric("Average target", f"{view['target'].mean():.1f}")
g = view.assign(gap=view["target"] - view["level"])
biggest = g["gap"].max()
names = ", ".join(g[g["gap"] == biggest]["factor"])
c3.metric("Biggest gap", f"{biggest}")
c3.caption(names)

long = view.melt(id_vars="factor", value_vars=["level", "target"],
                 var_name="series", value_name="score")
fig = px.line_polar(long, r="score", theta="factor",
                    color="series", line_close=True)
fig.update_traces(fill="toself")
fig.update_layout(polar=dict(radialaxis=dict(range=[0, 4], dtick=1)))

st.plotly_chart(fig, width="stretch")

# Evidence coverage: share of factors with any evidence, per track
st.subheader("Evidence coverage")
coverage = df.assign(has_evidence=df["evidence"].notna()).groupby("track")["has_evidence"].mean()
st.dataframe(coverage.map("{:.0%}".format))

# Evidence for the selected track
st.subheader(f"Evidence: {track}")
sorted_view = view.assign(has_evidence=view["evidence"].notna()).sort_values("has_evidence", ascending=False)
for _, row in sorted_view.iterrows():
    ev = row["evidence"]
    count = 0 if pd.isna(ev) else len(ev.split(";"))
    word = "piece" if count == 1 else "pieces"
    with st.expander(f"{row['factor']} · level {row['level']} · {count} {word}"):
        if pd.isna(ev):
            st.caption("No evidence yet.")
        else:
            for item in ev.split(";"):
                if item.startswith("http"):
                    st.markdown(f"[Open evidence]({item})")
                else:
                    st.markdown(Path(item).read_text(encoding="utf-8"))
                st.divider()
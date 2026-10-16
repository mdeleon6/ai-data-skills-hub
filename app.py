import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.title("Martino DeLeon: Data & AI Portfolio")
st.markdown(" Data analyst with 2.5 years at Ubisoft Halifax until the studio closed in 2026. Since then I've been building AI engineering projects alongside my analytics work, and I'm open to Data Analyst, AI Engineer, or hybrid roles. ")
st.caption("[Source on GitHub](https://github.com/mdeleon6/ai-data-skills-hub)")

# Projects first: each one starts with a question and answers it
st.subheader("Projects")
projects = pd.read_csv("projects.csv", keep_default_na=False).sort_values("order")
for _, p in projects.iterrows():
    with st.container(border=True):
        st.markdown(f"**{p['title']}**")
        st.markdown(f"*{p['question']}*")
        st.write(p["answer"])
        left, right = st.columns(2)
        if p["app_url"]:
            left.link_button("Live app", p["app_url"])
        right.link_button("Code & write-up", p["code_url"])

st.divider()
st.header("Skills map")
st.caption("Each score is backed by evidence. Pick a track, then open a factor below to see the proof.")



df = pd.read_csv("skills.csv")
evidence = pd.read_csv("evidence.csv")

# Across both tracks: one row per track
st.subheader("Overview")
summary = df.groupby("track")[["level", "target"]].mean().round(1)
summary["evidence pieces"] = evidence.merge(df, on="factor", how="inner").groupby("track").size()
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
coverage = df.assign(has_evidence=df["factor"].isin(evidence["factor"])).groupby("track")["has_evidence"].mean()
st.dataframe(coverage.map("{:.0%}".format))

# Evidence for the selected track
st.subheader(f"Evidence: {track}")
# LEFT JOIN: keep every factor in this track, even ones with no evidence yet
joined = view.merge(evidence, on="factor", how="left")
counts = joined.groupby("factor", sort=False)["url"].count()   # count() skips the empty (NaN) rows

for factor in counts.sort_values(ascending=False, kind="stable").index:
    pieces = joined[joined["factor"] == factor]
    level = pieces["level"].iloc[0]
    n = counts[factor]
    word = "piece" if n == 1 else "pieces"
    with st.expander(f"{factor} · level {level} · {n} {word}"):
        if n == 0:
            st.caption("No evidence yet.")
        for _, p in pieces.dropna(subset=["url"]).iterrows():
            with st.container(border=True):
                st.markdown(f"**{p['title']}**")
                st.caption(p["description"])
                if p["url"].startswith("http"):
                    st.link_button("Open", p["url"])
                else:
                    st.markdown(Path(p["url"]).read_text(encoding="utf-8"))
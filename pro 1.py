import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd

st.set_page_config(page_title="Entertainment Fan Network Analysis", layout="wide")

# ---------- HEADER ----------
# Project Description
st.markdown("""
### 📌 Project Scope
- Study fan communities online
- Combine: Graph + Community Detection
- Components: Fans (nodes), Connections (edges)
- Include: Influencer ranking, viral spread, clustering insights
""")

# ---------- HEADER ----------
st.markdown("""
# 🎬 Entertainment Fan Network Analysis Dashboard
### Professional Level Academic Project
""")

# ---------- INTRO ----------
st.markdown("""
This project analyzes **online fan communities** using **graph theory and network analysis**.

- **Nodes (Fans):** Represent individual users
- **Edges (Connections):** Represent interactions between fans
- **Goal:** Identify influencers, detect communities, and analyze content spread
""")

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Configuration")
num_users = st.sidebar.slider("Number of Fans", 10, 150, 40)
connection_prob = st.sidebar.slider("Connection Density", 0.01, 0.3, 0.07)

network_type = st.sidebar.selectbox("Network Model", ["Random Network", "Scale-Free Network (Influencer Driven)"])

# ---------- NETWORK CREATION ----------
if network_type == "Random Network":
    G = nx.erdos_renyi_graph(num_users, connection_prob)
else:
    G = nx.barabasi_albert_graph(num_users, max(1, int(num_users * connection_prob)))

# ---------- METRICS ----------
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
clustering = nx.clustering(G)

# ---------- COMMUNITY DETECTION ----------
from networkx.algorithms import community
communities = list(community.greedy_modularity_communities(G))

# ---------- LAYOUT ----------
pos = nx.spring_layout(G, seed=42)

# ---------- DASHBOARD METRICS ----------
st.subheader("📊 Network Overview")
col1, col2, col3 = st.columns(3)

col1.metric("Total Fans", G.number_of_nodes())
col2.metric("Total Connections", G.number_of_edges())
col3.metric("Detected Communities", len(communities))

# ---------- VISUALIZATION ----------
st.subheader("🌐 Network Visualization")

fig, ax = plt.subplots(figsize=(12, 8))

node_sizes = [v * 4000 for v in degree_centrality.values()]
node_colors = list(clustering.values())

nx.draw(
    G,
    pos,
    ax=ax,
    with_labels=False,
    node_size=node_sizes,
    node_color=node_colors,
    cmap=plt.cm.viridis,
    edge_color="gray"
)

st.pyplot(fig)

st.markdown("""
**Interpretation:**
- Larger nodes = Higher influence (degree centrality)
- Color intensity = Clustering coefficient (community strength)
- Dense clusters = Fan communities
""")

# ---------- INFLUENCER ANALYSIS ----------
st.subheader("🔥 Influencer Analysis")

top_influencers = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:7]

influencer_df = pd.DataFrame([
    {
        "Fan": f"Fan {node}",
        "Influence Score": round(score, 3),
        "Betweenness": round(betweenness[node], 3),
        "Clustering": round(clustering[node], 3)
    }
    for node, score in top_influencers
])

st.dataframe(influencer_df, use_container_width=True)

# ---------- COMMUNITY ANALYSIS ----------
st.subheader("👥 Community Detection")

community_data = []
for i, comm in enumerate(communities):
    community_data.append({
        "Community ID": i + 1,
        "Number of Fans": len(comm)
    })

st.dataframe(pd.DataFrame(community_data), use_container_width=True)

# ---------- CONTENT SPREAD SIMULATION ----------
st.subheader("🚀 Information Spread Simulation")

start_node = random.choice(list(G.nodes()))
visited = set([start_node])
queue = [start_node]
steps = 0

while queue and steps < 4:
    current = queue.pop(0)
    for neighbor in G.neighbors(current):
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
    steps += 1

st.write(f"Content originated from **Fan {start_node}**")
st.write(f"Total fans reached: **{len(visited)}** within {steps} steps")

# ---------- KEY INSIGHTS ----------
st.subheader("📌 Key Insights")
st.markdown("""
- Influencers (high centrality) accelerate content spread
- Communities represent clustered fan interests
- Scale-free networks better simulate real-world social media
- Network structure directly impacts virality
""")

# ---------- CONCLUSION ----------
st.subheader("📊 Conclusion")
st.markdown("""
This project demonstrates how **graph theory** can be applied to analyze entertainment fan networks. 
By identifying influencers and communities, we gain insights into audience behavior and content dissemination patterns.
""")

st.markdown("---")
st.caption("Professional Academic Project | Entertainment Fan Network Analysis")

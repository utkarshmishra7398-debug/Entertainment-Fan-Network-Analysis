import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random

st.set_page_config(page_title="Entertainment Fan Network Analysis", layout="wide")

# ---------- SESSION STATE ----------
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# ---------- TITLE & DESCRIPTION ----------
st.title("🎬 Entertainment Fan Network Analysis")

st.markdown("""
### 📌 About This Model
This model is used to analyze online entertainment fan communities.

**Key Features:**
- Study fan communities online  
- Combine: Graph + Community Detection  
- Components: Fans (nodes), Connections (edges)  
- Includes: Influencer ranking, viral spread, clustering insights  

👉 Enter input from sidebar and click **Run Analysis** to generate results.
""")

# ---------- SIDEBAR INPUT ----------
st.sidebar.header("📥 Input Parameters")
num_users = st.sidebar.slider("Number of Fans", 10, 100, 30)
connection_prob = st.sidebar.slider("Connection Probability", 0.01, 0.5, 0.1)

run_btn = st.sidebar.button("▶ Run Analysis")
reset_btn = st.sidebar.button("🔄 Reset")

# ---------- BUTTON LOGIC ----------
if run_btn:
    st.session_state.run_analysis = True

if reset_btn:
    st.session_state.run_analysis = False
    st.rerun()
# ---------- RUN ANALYSIS ----------
if st.session_state.run_analysis:
    
    # Create graph
    G = nx.erdos_renyi_graph(num_users, connection_prob)

    # Metrics
    centrality = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    # Top influencers
    top_influencers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]

    # Communities
    from networkx.algorithms import community
    communities = list(community.greedy_modularity_communities(G))

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # ---------- GRAPH ----------
    st.subheader("🌐 Fan Network Graph")

    fig, ax = plt.subplots(figsize=(10, 7))
    node_sizes = [v * 3000 for v in centrality.values()]

    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=False,
        node_size=node_sizes,
        node_color=list(centrality.values()),
        cmap=plt.cm.plasma,
        edge_color="gray"
    )

    st.pyplot(fig)

    # ---------- METRICS ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Fans", num_users)
    col2.metric("Connections", G.number_of_edges())
    col3.metric("Communities", len(communities))

    # ---------- INFLUENCERS ----------
    st.subheader("🔥 Influencer Ranking")

    df = pd.DataFrame([
        {"Fan": f"Fan {node}", "Influence Score": round(score, 3), "Betweenness": round(betweenness[node], 3)}
        for node, score in top_influencers
    ])

    st.dataframe(df, use_container_width=True)

    # ---------- COMMUNITIES ----------
    st.subheader("👥 Community Detection")

    comm_data = []
    for i, comm in enumerate(communities):
        comm_data.append({"Community": i+1, "Size": len(comm)})

    st.dataframe(pd.DataFrame(comm_data), use_container_width=True)

    # ---------- VIRAL SIMULATION ----------
    st.subheader("🚀 Viral Spread Simulation")

    start = random.choice(list(G.nodes()))
    visited = set([start])
    queue = [start]

    for _ in range(5):
        if not queue:
            break
        node = queue.pop(0)
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    st.write(f"Started from Fan {start}")
    st.write(f"Reached {len(visited)} fans in 5 steps")

    # ---------- INSIGHTS ----------
    st.subheader("📊 Insights")
    st.markdown("""
- Larger nodes = more influential fans  
- Communities show clustered fan groups  
- Influencers drive viral spread  
""")

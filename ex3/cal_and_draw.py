import csv
import networkx as nx
import matplotlib.pyplot as plt

# sorted_items=[]

def cal_draw():
    global sorted_items
    #创建一个有向图 
    G= nx.Graph()
    #读取CSV文件并添加边到图中
    with open('rel.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p1 = row ['p1']
            rel = row['rel']
            p2 = row ['p2']
            if p1 == ' p1' :
                continue
            G.add_edge(p1,p2,desc=rel)

    
    for i in nx.connected_components(G) :
        subg = G.subgraph(i)
        betweenness_centrality = nx.betweenness_centrality(subg)
        closeness_centrality = nx.closeness_centrality(subg)
        degree_centrality = nx.degree_centrality(subg)
        eigenvector_centrality =nx.eigenvector_centrality(subg)
        pagerank = nx.pagerank(subg)
    #计算核心节点
    en = {}
    for j in betweenness_centrality.keys():
        en[j] =betweenness_centrality[j]*0.2+closeness_centrality[j]*0.2+degree_centrality[j]*0.2
        +eigenvector_centrality[j]*0.2+pagerank[j]*0.2
    sorted_items = sorted(en.items(), key=lambda x: -x[1])

    plt.figure(figsize=(15,8))
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G,'desc')
    nx.draw(G, pos, with_labels=True,font_family='SimSun', node_size=1200)
    nx.draw_networkx_edge_labels(G, pos,font_family='SimSun', edge_labels=edge_labels)
    plt.savefig('rel.png')



if __name__ == '__main__':
    cal_draw()
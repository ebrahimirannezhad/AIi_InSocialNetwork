import urllib.request
import gzip
import networkx as nx
import random
from matplotlib import pyplot as plt


# آدرس فایل دانلود
url = "http://snap.stanford.edu/data/email-Eu-core.txt.gz"
file_name = "email-Eu-core.txt.gz"

# دانلود فایل
urllib.request.urlretrieve(url, file_name)

# استخراج فایل فشرده
with gzip.open(file_name, "rb") as f_in:
    with open("email-Eu-core.txt", "wb") as f_out:
        f_out.write(f_in.read())

# بارگیری مجموعه داده با استفاده از NetworkX
G = nx.read_edgelist("email-Eu-core.txt", create_using=nx.DiGraph())

# 1 Number of nodes
# 2 Number of edges
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print("Number of nodes:", num_nodes)
print("Number of edges:", num_edges)
# -------------------------------------------
# -------------------------------------------
# 3 In-degree, out-degree and degree of the first five nodes
# درجه ورودی، درجه خروجی و درجه برای پنج گره اول
for node in list(G.nodes())[:5]:
    in_degree = G.in_degree(node)
    out_degree = G.out_degree(node)
    degree = G.degree(node)
    print("Node:", node)
    print("In-degree:", in_degree)
    print("Out-degree:", out_degree)
    print("Degree:", degree)
    print("---------------------------")
# -------------------------------------------
# -------------------------------------------
# 4 Number of source nodes
# # شمارش تعداد گره‌های منبع
num_source_nodes = sum(in_degree == 0 for node, in_degree in G.in_degree())
print("Number of source nodes:", num_source_nodes)
# -------------------------------------------
# -------------------------------------------
# 5 Number of sink nodes
# # شمارش تعداد گره‌های مقصد
num_sink_nodes = sum(out_degree == 0 for node, out_degree in G.out_degree())
print("Number of sink nodes:", num_sink_nodes)
# -------------------------------------------
# -------------------------------------------
# 6 Number of isolated nodes
# # شمارش تعداد گره‌های تنها
num_isolated_nodes = sum(degree == 0 for node, degree in G.degree())
print("Number of isolated nodes:", num_isolated_nodes)
# -------------------------------------------
# -------------------------------------------
# 7 In-degree distribution
# # محاسبه توزیع درجه ورودی
in_degree_sequence = [in_degree for (node, in_degree) in G.in_degree()]
in_degree_counts = dict()
for degree in in_degree_sequence:
    if degree in in_degree_counts:
        in_degree_counts[degree] += 1
    else:
        in_degree_counts[degree] = 1

# نمایش نمودار توزیع درجه ورودی
plt.bar(in_degree_counts.keys(), in_degree_counts.values())
plt.xlabel("In-degree")
plt.ylabel("Count")
plt.title("In-degree Distribution")
plt.show()
# -------------------------------------------
# -------------------------------------------
# 8 Out-degree distribution
# # محاسبه توزیع درجه خروجی
out_degree_sequence = [out_degree for (node, out_degree) in G.out_degree()]
out_degree_counts = dict()
for degree in out_degree_sequence:
    if degree in out_degree_counts:
        out_degree_counts[degree] += 1
    else:
        out_degree_counts[degree] = 1

# نمایش نمودار توزیع درجه خروجی
plt.bar(out_degree_counts.keys(), out_degree_counts.values())
plt.xlabel("Out-degree")
plt.ylabel("Count")
plt.title("Out-degree Distribution")
plt.show()
# -------------------------------------------
# -------------------------------------------
# 9 Average degree, average in-degree and average out-degree
# محاسبه میانگین درجه
average_degree = sum(degree for (node, degree) in G.degree()) / len(G)
print("میانگین درجه:", average_degree)
#
# # محاسبه میانگین درجه ورودی
average_in_degree = sum(in_degree for (node, in_degree) in G.in_degree()) / len(G)
print("میانگین درجه ورودی:", average_in_degree)
#
# # محاسبه میانگین درجه خروجی
average_out_degree = sum(out_degree for (node, out_degree) in G.out_degree()) / len(G)
print("میانگین درجه خروجی:", average_out_degree)
# -------------------------------------------
# -------------------------------------------
# 10 Distance between five pairs of random nodes
# انتخاب پنج جفت تصادفی از گره‌ها
random_pairs = random.sample(list(G.nodes()), k=5)

# محاسبه فاصله بین جفت‌های تصادفی
for pair in random_pairs:
    source, target = pair
    distance = nx.shortest_path_length(G, source=source, target=target)
    print(f"فاصله بین گره {source} و گره {target}: {distance}")
# -------------------------------------------
# -------------------------------------------
# 11 Shortest path length distribution
# محاسبه توزیع طول مسیر کوتاهترین مسیر
shortest_path_lengths = dict(nx.shortest_path_length(G))
path_length_counts = dict()
for node in shortest_path_lengths:
    for path_length in shortest_path_lengths[node].values():
        if path_length in path_length_counts:
            path_length_counts[path_length] += 1
        else:
            path_length_counts[path_length] = 1

# نمایش نمودار توزیع طول مسیر کوتاهترین مسیر
plt.bar(path_length_counts.keys(), path_length_counts.values())
plt.xlabel("Path Length")
plt.ylabel("Count")
plt.title("Shortest Path Length Distribution")
plt.show()
# -------------------------------------------
# -------------------------------------------
# 12 Diameter
# محاسبه کوتاه‌ترین مسیرها بین تمام جفت گره‌ها
all_pairs_shortest_paths = dict(nx.all_pairs_shortest_path_length(G))

# یافتن مسیرهای بزرگترین طول
longest_path_length = 0
for source, paths in all_pairs_shortest_paths.items():
    for target, length in paths.items():
        if length > longest_path_length:
            longest_path_length = length

print("قطر شبکه:", longest_path_length)
# -------------------------------------------
# -------------------------------------------
# 13 Is the graph strongly connected? If so, compute the strongly connected component size distribution
# بررسی قابلیت دسترسی کامل
is_strongly_connected = nx.is_strongly_connected(G)

if is_strongly_connected:
    print("گراف قابل دسترسی کامل است")

    # محاسبه توزیع اندازه مؤلفه‌های قویا متصل
    strongly_connected_components = nx.strongly_connected_components(G)
    component_sizes = [len(component) for component in strongly_connected_components]
    component_sizes.sort(reverse=True)

    print("توزیع اندازه مؤلفه‌های قویا متصل:", component_sizes)
else:
    print("گراف قابل دسترسی کامل نیست")
# -------------------------------------------
# -------------------------------------------
# 14 Is the graph weakly connected? If so, compute the weakly connected component
# size distribution
# بررسی قابلیت دسترسی ضعیف
is_weakly_connected = nx.is_weakly_connected(G)

if is_weakly_connected:
    print("گراف قابل دسترسی ضعیف است")

    # محاسبه توزیع اندازه مؤلفه‌های ضعیفا متصل
    weakly_connected_components = nx.weakly_connected_components(G)
    component_sizes = [len(component) for component in weakly_connected_components]
    component_sizes.sort(reverse=True)

    print("توزیع اندازه مؤلفه‌های ضعیفا متصل:", component_sizes)
else:
    print("گراف قابل دسترسی ضعیف نیست")
# -------------------------------------------
# -------------------------------------------
# 15 Number of bridge edges
# محاسبه تعداد یال‌های پل
bridge_edges = list(nx.bridges(G))

num_bridge_edges = len(list(bridge_edges))

print("Number of bridge edges:", num_bridge_edges)

# -------------------------------------------
# -------------------------------------------
# 16 Number of articulation nodes
# محاسبه تعداد گره‌های مهم
articulation_nodes = list(nx.articulation_points(G))

num_articulation_nodes = len(list(articulation_nodes))

print("تعداد گره‌های مهم:", num_articulation_nodes)
# -------------------------------------------
# -------------------------------------------
# 17 Number of nodes in I n(v) for five random nodes
# # تعداد گره‌ها در مجموعه ورودی I n(v)
random_nodes = [1, 2, 3, 4, 5]  # لیست پنج گره تصادفی

for node in random_nodes:
    in_neighbors = [n for n, _ in G.in_edges(node)]
    num_in_neighbors = len(in_neighbors)
    print(f"Number of nodes in I n({node}): {num_in_neighbors}")
# -------------------------------------------
# -------------------------------------------
# 18 Number of nodes in Out(v) for five random nodes
# تعداد گره‌ها در مجموعه‌ی خروجی برای پنج گره تصادفی
random_nodes = [1, 2, 3, 4, 5]  # لیست پنج گره تصادفی
for node in random_nodes:
    out_neighbors = len(G.successors(node))
    print(f"Number of nodes in Out({node}): {out_neighbors}")
# -------------------------------------------
# -------------------------------------------
# 19 Clustering coefficient for five random nodes
# ضریب خوشه‌بندی برای پنج گره تصادفی
random_nodes = [1, 2, 3, 4, 5]  # لیست پنج گره تصادفی

clustering_coefficient = nx.average_clustering(G)
print("Clustering coefficient:", clustering_coefficient)
# -------------------------------------------
# -------------------------------------------
# 20 Clustering coefficient distribution
# محاسبه ضریب خوشه‌بندی برای همه گره‌ها
clustering_coefficients = nx.clustering(G)

# توزیع ضریب خوشه‌بندی
distribution = dict()
for cc in clustering_coefficients.values():
    distribution[cc] = distribution.get(cc, 0) + 1

# چاپ توزیع ضریب خوشه‌بندی
print("Clustering Coefficient Distribution:")
for cc, count in distribution.items():
    print(f"Coefficient: {cc} \t Count: {count}")
# -------------------------------------------
# -------------------------------------------
# 21 Average clustering coefficient
# محاسبه ضریب خوشه‌بندی برای همه گره‌ها
clustering_coefficients = nx.clustering(G)

# محاسبه میانگین ضریب خوشه‌بندی
average_clustering_coefficient = sum(clustering_coefficients.values()) / len(clustering_coefficients)

# چاپ میانگین ضریب خوشه‌بندی
print("Average Clustering Coefficient:", average_clustering_coefficient)

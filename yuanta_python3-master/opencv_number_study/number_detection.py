import numpy as np
import cv2

# 读取图片转为灰度图
img = cv2.imread('digits.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 把图片分隔成5000个，每个20x20大小
cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]

# 再转成numpy数组
x = np.array(cells)

# 一半用来训练的数组，一半用来测试的数组
train = x[:, :50].reshape(-1, 400).astype(np.float32)
test = x[:, 50:100].reshape(-1, 400).astype(np.float32)

# 创建训练和测试的标签
k = np.arange(10)
train_labels = np.repeat(k, 250)[:, np.newaxis]
test_labels = train_labels.copy()

# 创建一个K-Nearest Neighbour分类器，训练数据，然后用测试数据测试它
knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)
ret, result, neighbours, dist = knn.findNearest(test, k=5)

# 最终检查测试的精确度，比较结果，检查哪些是错误的，最终输出正确率
matches = result == test_labels
correct = np.count_nonzero(matches)
accuracy = correct * 100.0 / result.size

print(accuracy)

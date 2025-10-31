import numpy as np
class GetData():
    def __init__(self,n_instance,n_cities):
        self.n_instance = n_instance
        self.n_cities = n_cities

    def generate_instances(self):
        """
        Sinh ra danh sách các bài toán TSP ngẫu nhiên.

        Hàm này tạo `n_instance` bài toán TSP, mỗi bài toán gồm:
        - Một tập tọa độ 2D ngẫu nhiên cho `n_cities` thành phố.
        - Ma trận khoảng cách Euclidean giữa các thành phố.
        Returns:
            list[tuple[np.ndarray, np.ndarray]]: 
                Danh sách các instance, mỗi phần tử là (coordinates, distances)
                trong đó:
                - coordinates: mảng (n_cities, 2)
                - distances: ma trận (n_cities, n_cities)
        """
        np.random.seed(2025)
        instance_data = []
        for _ in range(self.n_instance):
            coordinates = np.random.rand(self.n_cities, 2)
            distances = np.linalg.norm(coordinates[:, np.newaxis] - coordinates, axis=2)
            instance_data.append((coordinates,distances))
        return instance_data
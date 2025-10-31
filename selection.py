import random
def parent_selection(pop,m):
    
    """
    Chọn ngẫu nhiên m cá thể cha mẹ từ quần thể (population) dựa trên xác suất tỉ lệ nghịch với thứ hạng.

    Tham số:
        pop (list): Danh sách các cá thể (population) hiện tại.
        m (int): Số lượng cá thể cha mẹ cần chọn.

    Quy trình:
        1. Gán thứ hạng cho từng cá thể trong quần thể (0, 1, 2, ..., len(pop)-1).
        2. Tính xác suất chọn cho từng cá thể theo công thức:
              probs[i] = 1 / (rank_i + 1 + len(pop))
           → Cá thể có thứ hạng nhỏ hơn (rank nhỏ hơn) sẽ có xác suất cao hơn một chút.
        3. Sử dụng hàm random.choices để chọn ngẫu nhiên m cá thể theo phân bố xác suất này.

    Returns:
        list: Danh sách gồm m cá thể được chọn làm cha mẹ.
    """
    ranks = [i for i in range(len(pop))]
    probs = [1 / (rank + 1 + len(pop)) for rank in ranks]
    parents = random.choices(pop, weights=probs, k=m)
    return parents
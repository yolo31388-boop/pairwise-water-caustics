import math


def refract_uv(uv, normal, strength):
    """折射 UV：用当前帧的统一法线偏移屏幕坐标。"""
    u, v = uv
    nx, ny = normal
    return (u + nx * strength, v + ny * strength)


def path_length(depth, view_z):
    """视线路径长度：沿视线的深度除以视距分量。"""
    if view_z == 0:
        return 0.0
    return depth / view_z


def absorption(distance, density):
    """水体吸收：按视线路径长度做指数积分。"""
    return math.exp(-density * distance)


def caustic_facing(normal_z, threshold):
    """焦散朝向：仅当法线朝向水面之上时才投影焦散。"""
    return normal_z >= threshold


def foam_mask(depth, object_id):
    """泡沫区域：靠近水面的深度且该像素带有物体标记。"""
    return depth < 0.5 and object_id != 0


def reflect_camera_position(y, plane_y):
    """反射相机高度：关于水面平面镜像主相机。"""
    return 2.0 * plane_y - y


def screen_edge_alpha(distance, fade):
    """屏幕边缘淡出：以 fade 为距离做线性软过渡。"""
    if fade <= 0:
        return 0.0
    return max(0.0, min(1.0, distance / fade))


def water_sort_key(layer, depth):
    """水面透明排序：先按水面层，再按深度由远及近。"""
    return (layer, -depth)


def temporal_reset(wave_speed, threshold):
    """时域重置：波浪变化超过阈值时丢弃历史累积。"""
    return wave_speed > threshold


def specular_once(base, reflection):
    """高光合成：反射项只叠加一次，避免重复乘。"""
    return base + reflection


def wave_normal_height(height, wavelength):
    """波浪法线：由高度与波长归一化得到坡度。"""
    if wavelength == 0:
        return 0.0
    return height / wavelength


def refraction_depth(current, previous):
    """折射深度选择：优先使用当前帧深度，无效时回退上一帧。"""
    return current if current > 0 else previous


def caustic_scale(depth, base):
    """焦散尺度：随水深受缩放，远处聚焦更大。"""
    if depth == 0:
        return 0.0
    return base / depth


def shoreline_alpha(depth, width):
    """岸线 alpha：在宽度范围内做软过渡，避免硬阈值锯齿。"""
    if width <= 0:
        return 0.0
    return max(0.0, min(1.0, depth / width))


def camera_matrix_key(camera_id):
    """相机矩阵键：每台相机各自持有独立的反射矩阵。"""
    return camera_id

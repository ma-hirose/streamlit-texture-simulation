
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from stl import mesh
import tempfile

# 初回実行時にsession_stateにカメラ眼位置を設定（必要なら他のパラメータも）
if 'camera_eye_x' not in st.session_state:
    st.session_state.camera_eye_x = -1.2
if 'camera_eye_y' not in st.session_state:
    st.session_state.camera_eye_y = -1.2
if 'camera_eye_z' not in st.session_state:
    st.session_state.camera_eye_z = 1.2

st.title("Texture Simulation with Streamlit")
st.markdown("")

# Sidebar read file or defalut
uploaded_file = st.sidebar.file_uploader("Upload your STL file", type=["stl"])

# アップロードされたファイルがあれば、一時ファイルとして保存し、そのパスを利用する
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp:
        tmp.write(uploaded_file.read())
        tmp.flush()
        stl_filepath = tmp.name
    st.sidebar.success("Success！")
else:
    stl_filepath = 'sample.stl'
    # st.sidebar.info("If there is no upload, use [3200_output.stl] as a default.")

# STL file reading
try:
    your_mesh = mesh.Mesh.from_file(stl_filepath)
except Exception as e:
    st.error(f"STLファイルの読み込みエラー: {e}")
    st.stop()

triangles = your_mesh.vectors
n_triangles = triangles.shape[0]
vertices = triangles.reshape(-1, 3)
x = vertices[:, 0]
y = vertices[:, 1]
z = vertices[:, 2]
faces = np.arange(n_triangles * 3).reshape(n_triangles, 3)
i = faces[:, 0]
j = faces[:, 1]
k = faces[:, 2]

# parameter setting
st.sidebar.header("Setting")
colors_list = [
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
    'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
    'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
    'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
    'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
    'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
    'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
    'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
    'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
    'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
    'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple',
    'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue',
    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
    'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
    'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
    'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen',
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen'
]
selected_color = st.sidebar.selectbox("Color", colors_list, index=colors_list.index("lightpink"))
opacity_val = st.sidebar.slider("Opacity", 0.0, 1.0, value=1.0, step=0.05)
ambient_val = st.sidebar.slider("Ambient", 0.0, 1.0, value=0.5, step=0.05)
diffuse_val = st.sidebar.slider("Diffuse", 0.0, 1.0, value=1.0, step=0.05)
roughness_val = st.sidebar.slider("Roughness", 0.0, 1.0, value=0.5, step=0.05)
specular_val = st.sidebar.slider("Specular", 0.0, 1.0, value=0.2, step=0.05)
st.session_state.camera_eye_x = st.sidebar.number_input("Camera Eye X", value=st.session_state.camera_eye_x, step=0.1, format="%.1f")
st.session_state.camera_eye_y = st.sidebar.number_input("Camera Eye Y", value=st.session_state.camera_eye_y, step=0.1, format="%.1f")
st.session_state.camera_eye_z = st.sidebar.number_input("Camera Eye Z", value=st.session_state.camera_eye_z, step=0.1, format="%.1f")

# Mesh3d
mesh3d = go.Mesh3d(
    x=x, y=y, z=z,
    i=i, j=j, k=k,
    opacity=opacity_val,
    color=selected_color,
    lighting=dict(
        ambient=ambient_val,
        diffuse=diffuse_val,
        roughness=roughness_val,
        specular=specular_val
    ),
)

fig = go.Figure(data=[mesh3d])
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=dict(eye=dict(
            x=st.session_state.camera_eye_x,
            y=st.session_state.camera_eye_y,
            z=st.session_state.camera_eye_z
        ))
    ),
    width=800, height=600,
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3D projection)


def rotation_matrix(axis: str, theta_deg: float) -> np.ndarray:
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)

    if axis == "x":
        return np.array([
            [1, 0,  0],
            [0, c, -s],
            [0, s,  c],
        ])
    elif axis == "y":
        return np.array([
            [ c, 0, s],
            [ 0, 1, 0],
            [-s, 0, c],
        ])
    elif axis == "z":
        return np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1],
        ])
    else:
        raise ValueError("axis must be 'x', 'y', or 'z'")


def plot_vectors(original: np.ndarray, rotated: np.ndarray):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    limit = max(np.abs(original).max(), np.abs(rotated).max(), 1.0) * 1.3

    ax.quiver(0, 0, 0, *original, color="steelblue", linewidth=2, label="Original")
    ax.quiver(0, 0, 0, *rotated, color="darkorange", linewidth=2, label="Rotated")

    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    ax.set_title("Original vs Rotated Vector")

    return fig


def main():
    st.set_page_config(page_title="3D Vector Rotation", layout="centered")
    st.title("3D Vector Rotation")
    st.write(
        "Enter a 3D vector, choose a rotation axis, and set the angle theta to see the rotated vector."
    )

    st.subheader("Input Vector")
    col1, col2, col3 = st.columns(3)
    with col1:
        vx = st.number_input("x", value=1.0, step=0.5)
    with col2:
        vy = st.number_input("y", value=0.0, step=0.5)
    with col3:
        vz = st.number_input("z", value=0.0, step=0.5)

    vector = np.array([vx, vy, vz], dtype=np.float64)

    st.subheader("Rotation Settings")
    axis = st.radio("Axis of rotation", options=["x", "y", "z"], horizontal=True)
    theta = st.slider("Theta (degrees)", min_value=-360.0, max_value=360.0, value=90.0, step=1.0)

    R = rotation_matrix(axis, theta)
    rotated_vector = R @ vector

    st.subheader("Result")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.write("**Original vector**")
        st.code(f"[{vx:.3f}, {vy:.3f}, {vz:.3f}]")
    with res_col2:
        st.write("**Rotated vector**")
        st.code(f"[{rotated_vector[0]:.3f}, {rotated_vector[1]:.3f}, {rotated_vector[2]:.3f}]")

    with st.expander("Show rotation matrix used"):
        st.write(f"Rotation about **{axis}**-axis by **{theta}°**:")
        st.write(np.round(R, 3))

    fig = plot_vectors(vector, rotated_vector)
    st.pyplot(fig)


if __name__ == "__main__":
    main()

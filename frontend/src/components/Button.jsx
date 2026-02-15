function Button({ label, color }) {
    const backgroundColor = color ? color : "#4f46e5";

    return (
        <button
        className="btn"
        style={{ backgroundColor }}
        >
        {label || "Button"}
        </button>
    );
}

export default Button;

export default function Table({ rows = 5, columns = 2 }) {
    const rowArray = Array.from({ length: rows });
    const colArray = Array.from({ length: columns });

    return (
        <table style={{
        borderCollapse: "collapse",
        width: "100%",
        maxWidth: "600px"
        }}>
        <thead>
            <tr>
            {colArray.map((_, i) => (
                <th key={i} style={{
                border: "1px solid #ddd",
                padding: "8px",
                background: "#f3f4f6"
                }}>
                Column {i + 1}
                </th>
            ))}
            </tr>
        </thead>
        <tbody>
            {rowArray.map((_, r) => (
            <tr key={r}>
                {colArray.map((_, c) => (
                <td key={c} style={{
                    border: "1px solid #ddd",
                    padding: "8px"
                }}>
                    Row {r + 1}, Col {c + 1}
                </td>
                ))}
            </tr>
            ))}
        </tbody>
        </table>
    );
}

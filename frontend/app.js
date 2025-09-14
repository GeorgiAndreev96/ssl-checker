function formatDate(dateStr) {
  if (!dateStr) return "N/A";
  const d = new Date(dateStr);
  const day = String(d.getDate()).padStart(2, "0");
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const year = d.getFullYear();
  return `${day}-${month}-${year}`;
}

function formatStatus(status) {
  if (status === "valid") return "Active";
  if (status === "error") return "Inactive / Error";
  return status;
}

document.getElementById("checkForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const url = document.getElementById("urlInput").value;
  try {
    const res = await fetch("/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    document.getElementById("result").innerText =
      `✅ ${data.domain} → Expires: ${formatDate(data.expiry)} → Status: ${formatStatus(data.status)}`;
    loadDomains();
  } catch (err) {
    document.getElementById("result").innerText = `❌ ${err.message}`;
  }
});

async function loadDomains() {
  try {
    const res = await fetch("/api/domains");
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const list = await res.json();
    const tbody = document.getElementById("domainList");
    tbody.innerHTML = "";
    list.forEach((d) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${d.domain}</td>
        <td>${formatStatus(d.status)}</td>
        <td>${formatDate(d.expiry)}</td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    document.getElementById("result").innerText = `❌ ${err.message}`;
  }
}

loadDomains();

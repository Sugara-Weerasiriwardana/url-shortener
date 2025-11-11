document.getElementById("shortenBtn").addEventListener("click", async () => {
  const longUrl = document.getElementById("longUrl").value;
  const resultDiv = document.getElementById("result");
  const statsDiv = document.getElementById("stats");
  statsDiv.classList.add("hidden");
  resultDiv.innerHTML = "Generating...";

  if (!longUrl) {
    resultDiv.innerHTML = "❗ Please enter a URL.";
    return;
  }

  try {
    const response = await fetch("/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ long_url: longUrl })
    });

    if (!response.ok) {
      resultDiv.innerHTML = "⚠️ Failed to shorten URL.";
      return;
    }

    const data = await response.json();
    const shortCode = data.short_code;
    const shortUrl = `${window.location.origin}/${shortCode}`;

    // Display short URL + buttons
    resultDiv.innerHTML = `
      ✅ Short URL: 
      <a href="${shortUrl}" target="_blank" class="text-blue-600 underline">${shortUrl}</a><br>
      <button id="copyBtn" class="mt-2 bg-green-500 text-white p-1 rounded hover:bg-green-600">Copy</button>
      <button id="viewStatsBtn" class="mt-2 bg-gray-200 p-1 rounded hover:bg-gray-300 ml-2">View Stats</button>
      <p id="copyMsg" class="text-sm text-gray-500 mt-1"></p>
    `;

    // Copy to clipboard logic
    document.getElementById("copyBtn").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(shortUrl);
        const copyMsg = document.getElementById("copyMsg");
        copyMsg.textContent = "✅ Copied to clipboard!";
        setTimeout(() => (copyMsg.textContent = ""), 2000);
      } catch (err) {
        console.error("Copy failed", err);
        document.getElementById("copyMsg").textContent = "❌ Copy failed";
      }
    });

    // Stats button logic
    document.getElementById("viewStatsBtn").addEventListener("click", async () => {
      statsDiv.classList.remove("hidden");
      document.getElementById("statCode").textContent = shortCode;
      document.getElementById("statClicks").textContent = "Loading...";

      try {
        const statsResponse = await fetch(`/stats/${shortCode}`);
        if (!statsResponse.ok) {
          document.getElementById("statClicks").textContent = "Error fetching stats.";
          return;
        }

        const statsData = await statsResponse.json();
        document.getElementById("statClicks").textContent = statsData.clicks;
      } catch (error) {
        console.error(error);
        document.getElementById("statClicks").textContent = "Error fetching stats.";
      }
    });

  } catch (error) {
    console.error(error);
    resultDiv.innerHTML = "❌ Error connecting to server.";
  }
});

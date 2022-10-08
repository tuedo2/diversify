
async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}


document.addEventListener("DOMContentLoaded", async () => {
    const currentTab = await getCurrentTab();

    const tweetURL = currentTab.url;

    if (tweetURL.includes("twitter.com/") && tweetURL.includes("/status/")) {
        const status = tweetURL.split("/status/")[1];
        document.getElementById('current-tweet').innerText = status;
    } else {
        document.getElementById('current-tweet').innerText = "This is not a tweet status!";
    }
});

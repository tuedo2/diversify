
const output_container = document.getElementById("output-container")
const button = document.querySelector("button")


const tweetsURL = "http://localhost:8000/tweets"

async function getCurrentURL() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab.url;
}

async function tweetsRequest(input) {
    const response = await fetch(tweetsURL, {
        mode: "cors",
        method: "POST",
        headers: {"Content-Type": "applications/json"},
        body: JSON.stringify(input),
    });

    const output = await response.json();
    console.log(output);

    output_container.innerHTML = output.text;
}

button.addEventListener("click", async() => {
    const input = { text: await getCurrentURL() };
    tweetsRequest(input);
})

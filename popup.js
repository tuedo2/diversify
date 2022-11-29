const tweet_status = document.getElementById("tweet-status");
const tweet_status_button = document.getElementById("tweet-status-button");

const article_list = document.getElementById("article-list");

const source_list = document.getElementById("source-list");
const source_list_button = document.getElementById("source-list-button");

const tweetsEndpoint = "http://localhost:8000/tweets"
const sourcesEndpoint = "http://localhost:8000/sources"

async function getCurrentURL() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab.url;
}

async function tweetsRequest(input) {
    const response = await fetch(tweetsEndpoint, {
        mode: "cors",
        method: "POST",
        headers: {"Content-Type": "applications/json"},
        body: JSON.stringify(input),
    });

    const output = await response.json();
    console.log(output);

    tweet_status.innerHTML = output.error;
    const num_articles = output.ids.length;

    article_list.innerHTML = "";
    for (var i = 0; i < num_articles; i++) {
        var id = output.ids[i];
        var text = output.texts[i];


        article_list.innerHTML += `<li>${text} (<a href="https://twitter.com/user/status/${id}"><it>link</it></a>)</li>`
    }
}

tweet_status_button.addEventListener("click", async() => {
    const input = { url: await getCurrentURL() };
    tweetsRequest(input);
})

async function sourcesRequest(input) {
    const response = await fetch(sourcesEndpoint, {
        mode: "cors",
        method: "POST",
        headers: {"Content-Type": "applications/json"},
        body: JSON.stringify(input),
    });

    const output = await response.json();
    console.log(output);

    source_list.innerHTML = output.error;
    for (var i = 0; i < output.sources.length; i++) {
        var source = output.sources[i];
        source_list.innerHTML += `<li><a href="https://twitter.com/${source}">@${source}</a></li>`;
    }
}

source_list_button.addEventListener("click", () => {
    let user = document.getElementById("input-username").value
    const input = { username: user };
    sourcesRequest(input);
})

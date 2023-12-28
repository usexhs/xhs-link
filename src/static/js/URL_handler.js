function resolveFullURL(fullURL) {
    document.getElementById("copied").innerText = '';
    document.getElementById("vru-error").innerText = '';

    // var fullURL = document.getElementById("fullurl").value;
    var expr = /xhslink\.com\/([a-zA-Z0-9]+)/gm;
    var regex = new RegExp(expr);

    if (fullURL.match(regex)) {
        document.getElementById("result").innerText = 'URL found, resolving...';

        fullURL = fullURL.match(regex);

        fetch(`/full/?url=${fullURL}`)
            .then(response => response.text())
            .then(data => {
                document.getElementById("result").innerText = `${data}`;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById("result").innerText = 'Error resolving the full URL.';
            });
    }
    else {
        document.getElementById("result").innerText = 'No valid URL found';
    }
};

function copyToClipboard() {
    document.getElementById("copied").innerText = '';
    /* Get the text field */
    var copyText = document.getElementById("result");

    // Select the text field
    // copyText.select();
    // copyText.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.innerText)
        .then(() => {
            document.getElementById("copied").innerText = 'Copied!';
        })
        .catch((err) => {
            document.getElementById("copied").innerText = 'Failed to Copy';
            console.error('Unable to copy text: ', err);
        });
};

function visitResolvedURL() {
    document.getElementById("vru-error").innerText = '';

    var ResolvedURL = document.getElementById("result").innerText;
    var expr = /www\.xiaohongshu\.com/gm;
    var regex = new RegExp(expr);

    if (ResolvedURL.match(regex)) {
        window.open(ResolvedURL, '_blank', 'noopener,noreferrer');
    }
    else {
        document.getElementById("vru-error").innerText = 'No valid URL found';
    }
}

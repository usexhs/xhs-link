<h1>xhslink Resolver</h1>

<p>Inspired by <a href="https://b23.wtf"><code>b23.wtf</code></a></p>

<p>Remove hidden tracking parameters in xhslink dot com.</p>
<p><strong>STILL UNDER INTENSIVE DEVELOPMENT</strong></p>

## Deploy Your Own

Go to [Deploy.md](./deploy.md)

<h2>Usage</h2>

<p>Suppose you have a link like: <code>(http(s)://)xhslink.com/YOUR_SHORT_CODE</code></p>

Here `YOUR_SHORT_CODE` should be an alphanumberic string, like

 - `o2s5so`
 - `TmtPSw`
 - `cUFu9d`
 - `kKsk`
 - `114514`

<strong>Redirect</strong>
<p>Replace "com" with "icu" in your link. </p>
<p><code>https://xhslink.icu/YOUR_SHORT_CODE</code></p>

<strong>API: Resolve the code</strong>
<p><code>https://xhs.li/code/YOUR_SHORT_CODE</code></p>

<strong>API: Resolve the full URL</strong>
<p><code>https://xhs.li/full/?url=(http(s)://)xhslink.com/YOUR_SHORT_CODE</code></p>

## License

![AGPLv3-icon](https://www.gnu.org/graphics/agplv3-155x51.png)

© Little Sweet Potato. This project is licensed under AGPLv3.

## Verify the Commits

Commits in this repo are signed by a PGP key. Get it [here](./lsp-public.asc).

// Cloudflare Pages Function (runs only for "/", see site/_routes.json).
// resume.jwong.org  -> serves the latest resume PDF at the root of that hostname.
// jwong.org         -> passes through to the normal static site.
// The PDF itself is a static file in the repo, rebuilt by GitHub Actions.
export async function onRequest({ request, env, next }) {
  const url = new URL(request.url);

  if (url.hostname === "resume.jwong.org") {
    url.pathname = "/jimmy.wong.resume.pdf";
    return env.ASSETS.fetch(new Request(url, request));
  }

  return next();
}

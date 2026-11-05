import { NextRequest, NextResponse } from "next/server";
export function proxy(request: NextRequest) {
  if (request.nextUrl.pathname === "/") {
    return NextResponse.redirect(new URL("/fa", request.url));
  }
  if (
    request.nextUrl.pathname === "/bff" ||
    request.nextUrl.pathname.startsWith("/bff/")
  )
    return NextResponse.json(
      { code: "NOT_FOUND" },
      { status: 404, headers: { "Cache-Control": "no-store" } },
    );
  const nonce = Buffer.from(
    crypto.getRandomValues(new Uint8Array(24)),
  ).toString("base64");
  const policy = `default-src 'self'; script-src 'self' 'nonce-${nonce}' 'strict-dynamic'; style-src 'self' 'nonce-${nonce}'; style-src-attr 'none'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'`;
  const headers = new Headers(request.headers);
  headers.set("x-nonce", nonce);
  headers.set("Content-Security-Policy", policy);
  const response = NextResponse.next({ request: { headers } });
  response.headers.set("Content-Security-Policy", policy);
  response.headers.set("Cache-Control", "no-store");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "no-referrer");
  return response;
}
export const config = { matcher: ["/((?!_next|fonts|favicon.ico).*)"] };

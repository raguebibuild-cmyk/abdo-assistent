import { google } from "googleapis";
import * as http from "http";
import { URL } from "url";

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID!;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET!;
const REDIRECT_URI = "http://localhost:3000/callback";

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error("Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in .env");
  process.exit(1);
}

const oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

const authUrl = oauth2Client.generateAuthUrl({
  access_type: "offline",
  scope: ["https://www.googleapis.com/auth/spreadsheets"],
  prompt: "consent",
});

console.log("\nOpen this URL in your browser:\n");
console.log(authUrl);
console.log("\nWaiting for callback on http://localhost:3000/callback ...\n");

const server = http.createServer(async (req, res) => {
  const params = new URL(req.url!, "http://localhost:3000").searchParams;
  const code = params.get("code");

  if (!code) {
    res.writeHead(400);
    res.end("No code in callback URL.");
    return;
  }

  try {
    const { tokens } = await oauth2Client.getToken(code);
    console.log("\n--- Add this to .env ---");
    console.log(`GOOGLE_REFRESH_TOKEN=${tokens.refresh_token}`);
    console.log("------------------------\n");
    res.writeHead(200);
    res.end("Done. You can close this tab and return to the terminal.");
  } catch (err) {
    console.error("Token exchange failed:", err);
    res.writeHead(500);
    res.end("Token exchange failed — check the terminal.");
  } finally {
    server.close();
  }
});

server.listen(3000);

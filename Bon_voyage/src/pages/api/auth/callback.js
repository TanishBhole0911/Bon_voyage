// Import your Auth0 handling logic
import { handleAuth } from "@auth0/nextjs-auth0";

export default async function callback(req, res) {
  try {
    // Handle authentication (e.g., using Auth0)
    const user = await handleAuth(req);
    console.log(user.email);
    // Redirect to the home route after successful authentication
    res.writeHead(302, { Location: "/home" });
    res.end();
  } catch (error) {
    console.error("Authentication failed:", error);
    res.status(500).json({ error: "Authentication failed" });
  }
}

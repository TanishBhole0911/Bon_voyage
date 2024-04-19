import Image from "next/image";
import { Inter } from "next/font/google";
import Login from "@/login";
import "../styles/globals.css";
const inter = Inter({ subsets: ["latin"] });

export default function dashboard() {
  return (
    <main
      className={` flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <h1 className="text-4xl font-bold">Welcome to Our Application</h1>
      <p className="text-2xl">This is the Getting Started page</p>
      <p className="text-xl">
        “Bon Voyage” is a travel-made-easy project that takes in account your
        suggestions and lets you take control by providing travel experience
        tailored to your own unique preferences
      </p>
      <Login className="login-btn" />
      <p className="text-xl">Your journey begins here</p>
    </main>
  );
}

import { useState } from "react";
import TagInput from "@/components/Taginput";
import "./index.css";
import { Button } from "@/components/ui/button";
import { useUser } from "@auth0/nextjs-auth0/client";
const axios = require("axios");
export default function Home() {
  const { user, error, isLoading } = useUser();
  const [interests, setInterests] = useState([]);
  const [healthIssues, setHealthIssues] = useState([]);
  const [foodPreferences, setFoodPreferences] = useState([]);
  const [responseData, setResponseData] = useState([]); // [response, setResponse]
  const handleSubmit = async (e) => {
    e.preventDefault();
    // console.log(e.target[0].value);
    // console.log(e.target[1].value);
    // console.log(e.target[2].value);
    // console.log(e.target[3].value);
    // console.log(interests.join(","));
    // console.log(healthIssues.join(","));
    // console.log(foodPreferences.join(","));

    //     {
    //     "Place": "Lucknow",
    //     "Food": "local",
    //     "Interests": "Adventure, Religion",
    //     "Health": "None",
    //     "Days": 5,
    //     "email": "abc@gmail.com",
    //     "in_date": "06-04-2024",
    //     "out_date": "06-04-2024"
    // }
    //get the difference between the dates
    const date1 = new Date(e.target[2].value);

    const date2 = new Date(e.target[3].value);
    const diffTime = Math.abs(date2 - date1);
    //change the date format from yyyy-mm-dd to dd-mm-yyyy
    const in_ = e.target[2].value.split("-").reverse().join("-");
    const out_ = e.target[3].value.split("-").reverse().join("-");
    console.log(diffTime);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    console.log(diffDays);
    fetch("http://localhost:3001/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Place: e.target[0].value,
        Food: foodPreferences.join(","),
        Interests: interests.join(","),
        Health: healthIssues.join(","),
        Days: 5,
        email: e.target[1].value,
        in_date: in_,
        out_date: out_,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setResponseData(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  return (
    <main className="main">
      <h1 className="title">Welcome to Bon Voyage</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Where are you going?"
          className="input location"
        />
        <input
          type="text"
          placeholder="Enter your email"
          className="input location"
        />
        <div className="dates">
          <div className="date-holder">
            <label htmlFor="datego">When are you going?</label>
            <input
              type="date"
              placeholder="When are you going?"
              className="input date-go"
            />
          </div>
          <div className="date-holder">
            <label htmlFor="dateback">When are you coming back?</label>
            <input
              type="date"
              placeholder="When are you coming back?"
              className="input date-back"
            />
          </div>
        </div>
        <TagInput
          _placeholder="Health Issues"
          tags={healthIssues}
          setTags={setHealthIssues}
          className="tag-input HealthIssues"
        />
        <TagInput
          _placeholder="Interest"
          tags={interests}
          setTags={setInterests}
          className="tag-input Interests"
        />
        <TagInput
          _placeholder="Food Preferences"
          tags={foodPreferences}
          setTags={setFoodPreferences}
          className="tag-input Preferences"
        />
        <button type="submit" className="submit-button">
          Plan my trip
        </button>
        {/* <Button type="submit" className="submit-button">
          Plan my trip
        </Button> */}
      </form>
      {responseData && (
        <div
          style={{
            backgroundColor: "black",
            color: "lightgreen",
            padding: "10px",
            marginTop: "20px",
          }}
        >
          {responseData}
        </div>
      )}
      <p className="description">Your one-stop shop for travel planning</p>
    </main>
  );
}

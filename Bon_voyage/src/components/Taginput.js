import React, { useEffect, useState } from "react";
const TagInput = ({ _placeholder, tags, setTags }) => {
  const [input, setInput] = useState("");
  const handleInputChange = (e) => {
    setInput(e.target.value);
  };
  const handleTagRemove = (event, tagToRemove) => {
    event.preventDefault();
    setTags(tags.filter((tag) => tag !== tagToRemove));
  };
  const handleInputKeyDown = (e) => {
    if (e.key === "Enter" && input !== "") {
      e.preventDefault();
      //console.log(tags);
      setTags([...tags, input]);
      setInput("");
      // console.log(tags);
    }
  };
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        width: "100%",
        color: "black",
        flexwrap: "wrap",
        justifyContent: "start",
        gap: "16px",
      }}
    >
      <input
        className="p-4 border border-gray-300 rounded-lg mt-4 text-black"
        type="text"
        value={input}
        placeholder={_placeholder}
        onChange={handleInputChange}
        onKeyDown={handleInputKeyDown}
        style={{ color: "black", marginRight: "auto", marginLeft: "auto" }}
      />
      {tags.map((tag, index) => (
        <div
          key={index}
          style={{
            display: "flex",
            justifyContent: "space-between",
            padding: "16px",
            marginBottom: "0px",
            marginTop: "16px",
            marginRight: "auto",
            minmarginRight: "10px",
            minmarginLeft: "10px",
            marginLeft: "auto",
            color: "black",
            width: "150px",
            backgroundColor: "#f2f2f2",
            borderRadius: "5px",
          }}
        >
          {tag}
          <span onClick={(event) => handleTagRemove(event, tag)}>x</span>
        </div>
      ))}
    </div>
  );
};

export default TagInput;

import React from "react";

const Tag = ({ label }) => {
  return (
    <div className="text-white">
      <span className="text-white">{label}</span>
      <button>×</button>
    </div>
  );
};

export default React.memo(Tag);

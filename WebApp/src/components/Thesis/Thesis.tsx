import React, { useState } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack5";
import { AiOutlineRight, AiOutlineLeft, AiOutlineDownload } from "react-icons/ai";
import "./Thesis.scss";
import Slider from "@mui/material/Slider";

export interface ThesisProps {}

const Thesis: React.FC<ThesisProps> = ({}) => {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState<number>(1.0);
  const [slide, setSlide] = useState<number>(1);
  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages);
    return true;
  }

  function handleRight() {
    if (numPages !== null && pageNumber < numPages)
      setPageNumber((prev) => prev + 1);
  }

  function handleLeft() {
    if (pageNumber !== 1) setPageNumber((prev) => prev - 1);
  }

  const handleChangeScale = (
    event: Event | React.SyntheticEvent<Element, Event>,
    newValue: number | number[]
  ) => {
    setScale(newValue as number);
  };

  const handleSlide = (event: Event, newValue: number | number[]) => {
    setSlide(newValue as number);
  };
  return (
    <div
      style={{
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: "256",
      }}
    >
      <div style={{ color: "#EEE", display: "flex", flexDirection: "column" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            columnGap: "3vh",
          }}
        >
          <div> x1.0 </div>
          <Slider
            style={{ width: "10vw" }}
            value={slide}
            onChangeCommitted={handleChangeScale}
            onChange={handleSlide}
          />
          <div> x2.0 </div>
        </div>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div style={{ width: "5vw" }}>
          <AiOutlineLeft
            className="iconLeftRight"
            style={{ height: "3.25vw", color: "#EEE", cursor: "pointer" }}
            onClick={handleLeft}
          />
        </div>
        <Document
          file={require("../pdfs/Filip_Gacek_Engineering_Thesis.pdf")}
          onLoadSuccess={onDocumentLoadSuccess}
        >
          <Page pageNumber={pageNumber} scale={scale / 100 + 1.0} />
        </Document>
        <div style={{ width: "5vw", textAlign: "end" }}>
          <AiOutlineRight
            className="iconLeftRight"
            style={{ height: "3.25vw", color: "#EEE", cursor: "pointer" }}
            onClick={handleRight}
          />
        </div>
      </div>
      <p style={{color: '#EEE'}}> Page {pageNumber} of {numPages}</p>
      <a href={require('../pdfs/Filip_Gacek_Engineering_Thesis.pdf')} download='Virtual Chess Engine with Reinforcement Learning' style={{textDecoration: 'none'}}>
      <div style={{width: '7vw', height: '5vh', color: '#eee', border: '1px solid #EEE', display: 'flex', flexDirection: 'row', alignItems:'center', justifyContent: 'center', cursor: 'pointer', gap: '4px'}} 
      className='downloadThesis'
      >
          <span style={{fontWeight: '500'}}>Download </span>
          <AiOutlineDownload style={{height: '3vh', width: '3vh'}}/>
      </div></a>
    </div>
  );
};

export default Thesis;

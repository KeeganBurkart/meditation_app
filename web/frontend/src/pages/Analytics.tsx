import { useEffect, useState } from "react";
import {
  getConsistencyData,
  getMoodCorrelationData,
  getTimeOfDayData,
  getLocationFrequencyData,
  DateValuePoint,
  MoodCorrelationPoint,
  HourValuePoint,
  StringValuePoint,
} from "../services/api";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ScatterChart,
  Scatter,
  BarChart,
  Bar,
} from "recharts";

export default function Analytics() {
  const [consistency, setConsistency] = useState<DateValuePoint[]>([]);
  const [mood, setMood] = useState<MoodCorrelationPoint[]>([]);
  const [timeOfDay, setTimeOfDay] = useState<HourValuePoint[]>([]);
  const [locations, setLocations] = useState<StringValuePoint[]>([]);

  useEffect(() => {
    getConsistencyData().then(setConsistency);
    getMoodCorrelationData().then(setMood);
    getTimeOfDayData().then(setTimeOfDay);
    getLocationFrequencyData().then(setLocations);
  }, []);

  return (
    <main>
      <h1>Analytics</h1>
      <div style={{ display: "grid", gap: "2rem" }}>
        <div>
          <h2>Consistency Over Time</h2>
          <LineChart width={400} height={200} data={consistency}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date_str" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
        </div>
        <div>
          <h2>Mood Correlation</h2>
          <ScatterChart width={400} height={200}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="mood_before" type="number" />
            <YAxis dataKey="mood_after" type="number" />
            <Tooltip />
            <Scatter data={mood} fill="#82ca9d" />
          </ScatterChart>
        </div>
        <div>
          <h2>Time of Day Distribution</h2>
          <BarChart width={400} height={200} data={timeOfDay}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="hour" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </div>
        <div>
          <h2>Location Frequency</h2>
          <BarChart width={400} height={200} data={locations}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#82ca9d" />
          </BarChart>
        </div>
      </div>
    </main>
  );
}

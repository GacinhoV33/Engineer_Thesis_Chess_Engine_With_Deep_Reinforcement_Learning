import React from "react";
import ReactGA from "react-ga4";

const useAnalyticsEventTracker = (category: string="Blog category") => {
  const eventTracker = (action: string = "new_game", label: string = "new_game") => {
    ReactGA.event({category, action, label});
  }
  return eventTracker;
}
export default useAnalyticsEventTracker;
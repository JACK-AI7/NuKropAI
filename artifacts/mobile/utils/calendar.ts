export interface CropEvent {
  stage: string;
  month: string;
  activity: string;
  tips: string[];
}

export interface CropCalendar {
  crop: string;
  season: "Kharif" | "Rabi" | "Zaid";
  events: CropEvent[];
}

const CALENDARS: Record<string, CropCalendar[]> = {
  "Telangana": [
    {
      crop: "Rice",
      season: "Kharif",
      events: [
        { stage: "Sowing", month: "June-July", activity: "Nursery preparation and sowing", tips: ["Treat seeds with Carbendazim", "Ensure 3cm water depth"] },
        { stage: "Transplanting", month: "July-August", activity: "Moving seedlings to main field", tips: ["Plant 2-3 seedlings per hill", "Maintain 15x15cm spacing"] },
        { stage: "Tillering", month: "August-September", activity: "Applying first dose of Urea", tips: ["Weed control is critical now"] },
        { stage: "Harvesting", month: "November-December", activity: "Cutting and threshing", tips: ["Harvest when 80% of grains are golden"] },
      ]
    },
    {
      crop: "Cotton",
      season: "Kharif",
      events: [
        { stage: "Sowing", month: "June", activity: "Sowing in well-drained soil", tips: ["Use Bt-Cotton seeds", "Dibbling method recommended"] },
        { stage: "Growth", month: "July-September", activity: "Pest monitoring and weeding", tips: ["Watch for Pink Bollworm", "Inter-cultivation every 15 days"] },
        { stage: "Picking", month: "November-January", activity: "Manual picking of bolls", tips: ["Pick dry bolls only", "Avoid mixing with trash"] },
      ]
    }
  ]
};

export function getCalendarForRegion(state: string, crops: string[]): CropCalendar[] {
  const regionalCals = CALENDARS[state] || CALENDARS["Telangana"]; // Fallback to Telangana
  return regionalCals.filter(cal => crops.includes(cal.crop));
}

export function getUpcomingEvents(calendar: CropCalendar): CropEvent[] {
  // Simplified logic to find events matching current or next month
  // In a real app, this would use date comparison
  return calendar.events.slice(0, 2); 
}

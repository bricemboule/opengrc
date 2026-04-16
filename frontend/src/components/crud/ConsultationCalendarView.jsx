import { CalendarDays, Clock3, Link2, MapPin, PhoneCall, UsersRound } from "lucide-react";
import { useMemo, useState } from "react";
import { FiChevronLeft, FiChevronRight, FiExternalLink } from "react-icons/fi";
import EmptyState from "./EmptyState";

const WEEKDAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];
const MONTH_LABELS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const SHORT_MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function formatSentenceLabel(value) {
  const normalized = String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .trim();
  if (!normalized) return "";
  return normalized.charAt(0).toUpperCase() + normalized.slice(1);
}

function formatTitleLabel(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/(^|\s)\w/g, (character) => character.toUpperCase())
    .trim();
}

function parseWallClockValue(value) {
  if (!value) return null;

  const normalized = String(value).trim();
  if (!normalized) return null;

  const dateTimeMatch = normalized.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
  if (dateTimeMatch) {
    const [, year, month, day, hour, minute] = dateTimeMatch;
    const date = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), 0, 0);

    return {
      date,
      year: Number(year),
      month: Number(month),
      day: Number(day),
      hour: Number(hour),
      minute: Number(minute),
      hasTime: true,
    };
  }

  const dateMatch = normalized.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (dateMatch) {
    const [, year, month, day] = dateMatch;
    const date = new Date(Number(year), Number(month) - 1, Number(day), 0, 0, 0, 0);

    return {
      date,
      year: Number(year),
      month: Number(month),
      day: Number(day),
      hour: 0,
      minute: 0,
      hasTime: false,
    };
  }

  const parsed = new Date(normalized);
  if (Number.isNaN(parsed.getTime())) return null;

  return {
    date: parsed,
    year: parsed.getFullYear(),
    month: parsed.getMonth() + 1,
    day: parsed.getDate(),
    hour: parsed.getHours(),
    minute: parsed.getMinutes(),
    hasTime: true,
  };
}

function toDateValue(value) {
  return parseWallClockValue(value)?.date || null;
}

function getLocalDayKey(dateLike) {
  const source =
    dateLike instanceof Date
      ? {
          year: dateLike.getFullYear(),
          month: dateLike.getMonth() + 1,
          day: dateLike.getDate(),
        }
      : dateLike;

  return `${source.year}-${`${source.month}`.padStart(2, "0")}-${`${source.day}`.padStart(2, "0")}`;
}

function getWeekStart(date) {
  const result = new Date(date);
  const offset = (result.getDay() + 6) % 7;
  result.setDate(result.getDate() - offset);
  result.setHours(0, 0, 0, 0);
  return result;
}

function getMonthGrid(displayedMonth, itemsByDay) {
  const monthStart = new Date(displayedMonth.getFullYear(), displayedMonth.getMonth(), 1);
  const gridStart = getWeekStart(monthStart);
  const weeks = [];
  const today = getLocalDayKey(new Date());

  for (let weekIndex = 0; weekIndex < 6; weekIndex += 1) {
    const week = [];

    for (let dayIndex = 0; dayIndex < 7; dayIndex += 1) {
      const currentDate = new Date(gridStart);
      currentDate.setDate(gridStart.getDate() + weekIndex * 7 + dayIndex);
      const dayKey = getLocalDayKey(currentDate);
      week.push({
        dayKey,
        label: currentDate.getDate(),
        inCurrentMonth: currentDate.getMonth() === displayedMonth.getMonth(),
        isToday: dayKey === today,
        count: itemsByDay.get(dayKey)?.length || 0,
      });
    }

    weeks.push(week);
  }

  return weeks;
}

function formatDateHeading(value) {
  const parsed = parseWallClockValue(value);
  if (!parsed) return "No scheduled date";
  const weekday = parsed.date.toLocaleDateString([], { weekday: "long" });
  return `${weekday}, ${parsed.day} ${MONTH_LABELS[parsed.month - 1]}`;
}

function formatTimeLabel(hour, minute) {
  const meridiem = hour >= 12 ? "PM" : "AM";
  const normalizedHour = hour % 12 || 12;
  return `${normalizedHour}:${String(minute || 0).padStart(2, "0")} ${meridiem}`;
}

function formatDateTime(value) {
  const parsed = parseWallClockValue(value);
  if (!parsed) return "No time";
  return `${SHORT_MONTH_LABELS[parsed.month - 1]} ${parsed.day}, ${parsed.year}, ${formatTimeLabel(parsed.hour, parsed.minute)}`;
}

function formatTimeRange(startValue, endValue) {
  const start = parseWallClockValue(startValue);
  if (!start) return "No time set";

  const startLabel = formatTimeLabel(start.hour, start.minute);
  const end = parseWallClockValue(endValue);
  if (!end) return startLabel;

  return `${startLabel} - ${formatTimeLabel(end.hour, end.minute)}`;
}

function getStatusTone(status) {
  switch (String(status || "").toLowerCase()) {
    case "confirmed":
      return "bg-[#f2f0ec] text-[#6f685f]";
    case "scheduled":
    case "rescheduled":
      return "bg-[#f6eee6] text-[#86664f]";
    case "completed":
      return "bg-[#ecf6ef] text-[#486455]";
    case "missed":
      return "bg-[#f7ece9] text-[#845a53]";
    default:
      return "bg-[#f2f1ef] text-[#776f68]";
  }
}

function getChannelTone(channel) {
  switch (String(channel || "").toLowerCase()) {
    case "video":
      return "bg-[#f1eeff] text-[#6354b5]";
    case "hybrid":
      return "bg-[#eef7f0] text-[#356345]";
    case "phone":
      return "bg-[#fff3e7] text-[#8a6236]";
    default:
      return "bg-[#f2f1ef] text-[#776f68]";
  }
}

function buildUpcomingItems(rows) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return rows
    .map((row) => {
      const scheduleDate = toDateValue(row.start_datetime || row.planned_date);
      const followUpDate = toDateValue(row.next_follow_up_date);
      const anchorDate = scheduleDate || followUpDate;
      const attendeeLines = String(row.attendees || "")
        .split(/\r?\n/)
        .map((item) => item.trim())
        .filter(Boolean);

      return {
        ...row,
        scheduleDate,
        followUpDate,
        anchorDate,
        attendeeCount: attendeeLines.length,
        engagementChannelLabel: formatSentenceLabel(row.engagement_channel || "in_person"),
        consultationTypeLabel: formatTitleLabel(row.consultation_type),
        statusLabel: formatTitleLabel(row.status),
      };
    })
    .filter((row) => row.anchorDate && row.anchorDate >= today && !["archived"].includes(String(row.status || "").toLowerCase()))
    .sort((left, right) => left.anchorDate - right.anchorDate);
}

function buildSummary(items) {
  const now = new Date();
  const next14Days = new Date(now);
  next14Days.setDate(now.getDate() + 14);
  const next7Days = new Date(now);
  next7Days.setDate(now.getDate() + 7);

  return [
    {
      label: "Upcoming",
      value: items.filter((item) => item.scheduleDate && item.scheduleDate >= now && item.scheduleDate <= next14Days).length,
      helper: "Meetings in the next 14 days",
      tone: "bg-[#f0be7c]",
    },
    {
      label: "Follow-up due",
      value: items.filter((item) => item.followUpDate && item.followUpDate >= now && item.followUpDate <= next7Days).length,
      helper: "Next actions due within 7 days",
      tone: "bg-[#b8abff]",
    },
    {
      label: "Remote sessions",
      value: items.filter((item) => ["video", "hybrid", "phone"].includes(String(item.engagement_channel || "").toLowerCase())).length,
      helper: "Calls or remote meetings tracked",
      tone: "bg-[#93e1a4]",
    },
  ];
}

export default function ConsultationCalendarView({ rows = [] }) {
  const upcomingItems = useMemo(() => buildUpcomingItems(rows), [rows]);
  const [displayedMonth, setDisplayedMonth] = useState(() => {
    const baseDate = upcomingItems[0]?.anchorDate || new Date();
    return new Date(baseDate.getFullYear(), baseDate.getMonth(), 1);
  });

  const visibleUpcomingItems = useMemo(
    () => upcomingItems.filter((item) => item.anchorDate && item.anchorDate.getFullYear() === displayedMonth.getFullYear() && item.anchorDate.getMonth() === displayedMonth.getMonth()),
    [displayedMonth, upcomingItems],
  );

  const itemsByDay = useMemo(() => {
    const bucket = new Map();
    visibleUpcomingItems.forEach((item) => {
      const key = getLocalDayKey(item.anchorDate);
      const currentItems = bucket.get(key) || [];
      currentItems.push(item);
      bucket.set(key, currentItems);
    });
    return bucket;
  }, [visibleUpcomingItems]);

  const groupedItems = useMemo(() => {
    const groups = [];
    let currentKey = "";
    let currentGroup = null;

    visibleUpcomingItems.forEach((item) => {
      const key = getLocalDayKey(item.anchorDate);
      if (key !== currentKey) {
        currentKey = key;
        currentGroup = { key, label: formatDateHeading(item.anchorDate), items: [] };
        groups.push(currentGroup);
      }
      currentGroup.items.push(item);
    });

    return groups;
  }, [visibleUpcomingItems]);

  const summary = useMemo(() => buildSummary(upcomingItems), [upcomingItems]);
  const calendarWeeks = useMemo(() => getMonthGrid(displayedMonth, itemsByDay), [displayedMonth, itemsByDay]);

  if (!upcomingItems.length) {
    return <EmptyState title="No upcoming consultations" description="Scheduled meetings, calls, and follow-up actions will appear here once consultation records carry meeting dates." />;
  }

  return (
    <section className="space-y-6">
      <div className="grid gap-3 md:grid-cols-3">
        {summary.map((item) => (
          <article key={item.label} className="app-surface rounded-[20px] px-5 py-5">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-[11px] font-semibold text-[#554d46]">{item.label}</p>
                <p className="mt-3 text-[1.9rem] font-semibold tracking-[-0.05em] text-slate-950">{item.value}</p>
              </div>
              <span className={`h-3.5 w-3.5 rounded-full ${item.tone}`} />
            </div>
            <p className="mt-2 text-[12px] leading-5 text-[#5e5650]">{item.helper}</p>
          </article>
        ))}
      </div>

      <div className="flex gap-6">
        <aside className="app-surface rounded-[22px] p-5 w-80 h-fit">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-[11px] font-semibold text-[#554d46]">Calendar</p>
              <h3 className="mt-2 text-[1rem] font-semibold text-slate-950">Upcoming consultations</h3>
            </div>
            <CalendarDays size={17} className="text-black/62" />
          </div>

          <div className="mt-5 flex items-center justify-between gap-3">
            <button
              type="button"
              onClick={() => setDisplayedMonth((current) => new Date(current.getFullYear(), current.getMonth() - 1, 1))}
              className="flex h-8 w-8 items-center justify-center rounded-full bg-white/86 text-black/68 transition hover:bg-white hover:text-black"
            >
              <FiChevronLeft size={14} />
            </button>
            <strong className="text-[0.92rem] font-semibold text-black">
              {MONTH_LABELS[displayedMonth.getMonth()]} {displayedMonth.getFullYear()}
            </strong>
            <button
              type="button"
              onClick={() => setDisplayedMonth((current) => new Date(current.getFullYear(), current.getMonth() + 1, 1))}
              className="flex h-8 w-8 items-center justify-center rounded-full bg-white/86 text-black/68 transition hover:bg-white hover:text-black"
            >
              <FiChevronRight size={14} />
            </button>
          </div>

          <div className="mt-4 grid grid-cols-7 gap-1 text-center text-[11px] font-semibold text-black/38">
            {WEEKDAY_LABELS.map((label) => (
              <span key={label}>{label}</span>
            ))}
          </div>

          <div className="mt-2 space-y-1">
            {calendarWeeks.map((week, weekIndex) => (
              <div key={`${displayedMonth.getMonth()}-${weekIndex}`} className="grid grid-cols-7 gap-1">
                {week.map((day) => (
                  <div
                    key={day.dayKey}
                    className={`min-h-[46px] rounded-[12px] px-1.5 py-1.5 ${day.inCurrentMonth ? "bg-white/74" : "bg-white/38"}`}
                    title={day.count ? `${day.count} consultation${day.count > 1 ? "s" : ""}` : "No consultations"}
                  >
                    <div className={`text-[11px] font-semibold ${day.isToday ? "text-black" : day.inCurrentMonth ? "text-black/72" : "text-black/24"}`}>{day.label}</div>
                    {day.count ? (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {Array.from({ length: Math.min(day.count, 3) }).map((_, index) => (
                          <span key={`${day.dayKey}-${index}`} className="h-1.5 w-1.5 rounded-full bg-[#111111]" />
                        ))}
                        {day.count > 3 ? <span className="text-[10px] font-medium text-black/42">+{day.count - 3}</span> : null}
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </aside>

        <div className="app-surface rounded-[22px] p-5 flex-1">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-[11px] font-semibold text-[#554d46]">Upcoming list</p>
              <h3 className="mt-2 text-[1rem] font-semibold text-slate-950">Meetings, calls, and follow-up moments</h3>
              <p className="mt-1 text-[12px] leading-6 text-[#5e5650]">
                Only items scheduled in {MONTH_LABELS[displayedMonth.getMonth()]} {displayedMonth.getFullYear()} are shown below.
              </p>
              <p className="mt-1 text-[12px] leading-6 text-[#5e5650]">Use this view to see what is next, how to join it, and where follow-up is due.</p>
            </div>
          </div>

          <div className="mt-5 space-y-5">
            {groupedItems.length ? (
              groupedItems.map((group) => (
                <section key={group.key} className="space-y-3">
                  <div className="flex items-center gap-2">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#111111]" />
                    <h4 className="text-[0.95rem] font-semibold text-black">{group.label}</h4>
                  </div>

                  <div className="space-y-3">
                    {group.items.map((item) => (
                      <article key={item.id} className="rounded-[18px] bg-white/82 px-4 py-4">
                        <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                          <div className="min-w-0 space-y-2">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${getStatusTone(item.status)}`}>{item.statusLabel}</span>
                              <span className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${getChannelTone(item.engagement_channel)}`}>{item.engagementChannelLabel}</span>
                            </div>
                            <div>
                              <h5 className="text-[0.96rem] font-semibold text-slate-950">{item.title}</h5>
                              <p className="mt-1 text-[12px] leading-6 text-[#5e5650]">{[item.consultationTypeLabel, item.stakeholder_name].filter(Boolean).join(" • ") || "Consultation session"}</p>
                            </div>
                            <div className="flex flex-wrap gap-x-5 gap-y-2 text-[12px] text-[#5e5650]">
                              <span className="inline-flex items-center gap-2">
                                <Clock3 size={13} className="text-black/52" />
                                {formatTimeRange(item.start_datetime || item.planned_date, item.end_datetime)}
                              </span>
                              {item.meeting_location ? (
                                <span className="inline-flex items-center gap-2">
                                  <MapPin size={13} className="text-black/52" />
                                  {item.meeting_location}
                                </span>
                              ) : null}
                              {item.attendeeCount ? (
                                <span className="inline-flex items-center gap-2">
                                  <UsersRound size={13} className="text-black/52" />
                                  {item.attendeeCount} attendee{item.attendeeCount > 1 ? "s" : ""}
                                </span>
                              ) : null}
                              {item.dial_in_details && !item.meeting_link ? (
                                <span className="inline-flex items-center gap-2">
                                  <PhoneCall size={13} className="text-black/52" />
                                  Dial-in recorded
                                </span>
                              ) : null}
                            </div>
                            {item.next_follow_up_date ? <p className="text-[12px] text-black/56">Follow-up due {formatDateTime(item.next_follow_up_date)}</p> : null}
                          </div>

                          <div className="flex shrink-0 flex-wrap items-center gap-2 lg:justify-end">
                            {item.meeting_link ? (
                              <a
                                href={item.meeting_link}
                                target="_blank"
                                rel="noreferrer"
                                className="app-button app-button-dark app-button-sm"
                                style={{ paddingLeft: "1.15rem", paddingRight: "1.15rem", fontSize: "0.76rem" }}
                              >
                                <FiExternalLink size={13} />
                                Open link
                              </a>
                            ) : item.dial_in_details ? (
                              <span className="inline-flex items-center gap-2 rounded-full bg-[#f2f1ef] px-3 py-2 text-[11px] font-medium text-black/62" title={item.dial_in_details}>
                                <Link2 size={12} />
                                Dial-in ready
                              </span>
                            ) : null}
                          </div>
                        </div>
                      </article>
                    ))}
                  </div>
                </section>
              ))
            ) : (
              <EmptyState title={`No consultations in ${MONTH_LABELS[displayedMonth.getMonth()]}`} description="Move the calendar to another month or add new consultations to populate this agenda." />
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

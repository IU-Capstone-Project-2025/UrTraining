import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import '../css/CustomCalendar.css'
import { useMemo, type JSX } from 'react';
import type { TrackerProp } from './interface/TrackerInterface';

type TrainingCalendarProps = {
    schedule: TrackerProp[]
    onDateClick: (date: String) => void;
}

const formattedDate = (date: Date): string => {
  return date
    .toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    })
    .replace(/\//g, '.');
};

const TrainingCalendar: React.FC<TrainingCalendarProps>  = ({ schedule, onDateClick }) => {
  // Преобразуем данные в Map: 'DD.MM.YYYY' => [array of trainings]
    const trainingByDate = useMemo<Record<string, boolean>>(() => {

        console.log(schedule);

        const map: Record<string, boolean> = {};

        for (const { date } of schedule) {
            map[date] = true;
        }

        return map;

    }, [schedule]);

    const tileClassName = ({ date, view }: { date: Date; view: string }): string | null => {
        if (view !== 'month') return null;
        const formatted = formattedDate(date);
        return trainingByDate[formatted] ? 'training-day' : null;
    };

    const handleClick = (date: Date) => {
        const formatted = date.toLocaleDateString('ru-RU');
        console.log(formatted)
        if (trainingByDate[formatted]) {
            onDateClick(formatted);
        } 
    };

    return (
        <Calendar
            onClickDay={handleClick}
            tileClassName={tileClassName}
            locale="en-EN"
        />
    );
};

export default TrainingCalendar;

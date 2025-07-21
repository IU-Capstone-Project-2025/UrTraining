import { useNavigate, useParams } from "react-router-dom";
import { useContext } from "react";
import { useQuery } from "@tanstack/react-query";
import AuthContext from "../components/context/AuthContext";
import { getTrainingsByDateRequest } from "../api/apiRequests";
import TrainingsByDate from "../components/TrainingsByDate";
import type { TrackerWithDataProp } from "../components/interface/TrackerInterface";


const TrainingsByDatePage = () => {

    const { currentDate } = useParams();
    const authData = useContext(AuthContext);
    const navigate = useNavigate();

    const { data : trainingsByDate = [], isLoading: isLoadingTraining, status } = useQuery<TrackerWithDataProp[], Error>({
        queryKey: ['trainingsThisDay'],
        queryFn: () => getTrainingsByDateRequest(currentDate as String, authData.access_token),
        enabled: !!authData?.access_token && !!currentDate
    })

    console.log(currentDate);

    if (status == "success") {
        console.log(trainingsByDate);
    }

    return(
        <>
            {trainingsByDate.length > 0 ? (
                <TrainingsByDate
                    trainings={trainingsByDate}
                />
            ) : (
                <div className="centered-content">
                    <div className="step-title-main">Oops...</div>
                    <p>You have no training sessions for today, so it's time for rest or looking for new workouts and plans!</p>
                    <div className="button-group-welcome">
                        <button className="btn-basic-black" onClick={() => navigate("/catalogue")}>Go to catalogue</button>
                    </div>
                </div>
            )}
        </>
    );
};

export default TrainingsByDatePage;
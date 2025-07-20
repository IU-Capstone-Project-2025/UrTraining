import { useParams } from "react-router-dom";
import { useContext } from "react";
import { useQuery } from "@tanstack/react-query";
import AuthContext from "../components/context/AuthContext";
import { getTrainingsByDateRequest } from "../api/apiRequests";
import TrainingsByDate from "../components/TrainingsByDate";
import type { TrackerWithDataProp } from "../components/interface/TrackerInterface";


const TrainingsByDatePage = () => {

    const { currentDate } = useParams();
    const authData = useContext(AuthContext);

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
        <TrainingsByDate
            trainings={trainingsByDate}
        />
    );
};

export default TrainingsByDatePage;
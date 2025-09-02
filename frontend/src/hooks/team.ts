import { getUserTeams } from "../api/teams";
import { useQuery } from "@tanstack/react-query";

export const useGetUserTeam = () => {
  return useQuery({
    queryKey: ["userTeams"],
    queryFn: getUserTeams,
  });
};

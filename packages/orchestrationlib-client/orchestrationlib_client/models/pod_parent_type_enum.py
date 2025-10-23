from enum import Enum


class PodParentTypeEnum(str, Enum):
    CRONJOB = "cronjob"
    DAEMONSET = "daemonset"
    DEPLOYMENT = "deployment"
    JOB = "job"
    REPLICASET = "replicaset"
    STATEFULSET = "statefulset"

    def __str__(self) -> str:
        return str(self.value)

from dataclasses import dataclass


@dataclass
class EvaluationMetrics:
    total_queries: int = 0
    hit_at_1: int = 0
    hit_at_5: int = 0
    reciprocal_rank_sum: float = 0.0

    def update(self, rank: int | None):
        self.total_queries += 1

        if rank is None:
            return

        if rank == 1:
            self.hit_at_1 += 1

        if rank <= 5:
            self.hit_at_5 += 1

        self.reciprocal_rank_sum += 1.0 / rank

    def summary(self) -> dict:

        if self.total_queries == 0:
            return {
                "queries": 0,
                "hit@1": 0.0,
                "hit@5": 0.0,
                "mrr": 0.0,
            }

        return {
            "queries": self.total_queries,
            "hit@1": round(
                self.hit_at_1 / self.total_queries,
                4,
            ),
            "hit@5": round(
                self.hit_at_5 / self.total_queries,
                4,
            ),
            "mrr": round(
                self.reciprocal_rank_sum
                / self.total_queries,
                4,
            ),
        }

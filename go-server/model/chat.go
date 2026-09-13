package model

type ChatRequest struct {
	Content string `json:"content"`
}
type CurrentChunk struct {
	ID    int    `json:"id"`
	Chunk string `json:"chunk"`
}
type ChunkResponse struct {
	Chunks []CurrentChunk `json:"chunks"`
}

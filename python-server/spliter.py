def split_md(path: str):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks=[]
        current_chunks=[]
        for line in text.split("\n"):
                if line.startswith("#"):
                        if current_chunks:
                                chunks.append(
                                        "\n".join(current_chunks)
                                )
                        current_chunks=[]

                current_chunks.append(line)
        if current_chunks:
               chunks.append(
                      "\n".join(current_chunks)
               )
        return chunks


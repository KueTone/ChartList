import axios from "axios";

export const fetchBlockValues = async () => {
    const response = await axios.get("http://127.0.0.1:8000/block-values");
    return response.data.block_values;
};

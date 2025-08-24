import { GoodreadsWrapped } from "./types";
import LongestBinge from "./LongestBinge";
import ImpulseReads from "./ImpulseReads";

export default function WrappedPage({ data }: { data: GoodreadsWrapped }) {
    const Binge = Array.isArray(data.longest_binge_session) ? data.longest_binge_session: JSON.parse(data.longest_binge_session);
    const Impulse = Array.isArray(data.impulse_reads) ? data.impulse_reads: JSON.parse(data.impulse_reads);

    return (
        <div>
            <LongestBinge reads={Binge} />
            <ImpulseReads reads={Impulse}/>
        </div>
    );
}

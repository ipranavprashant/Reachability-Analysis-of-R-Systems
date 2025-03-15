/* eslint-disable react/prop-types */
import { useCallback, useMemo } from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";

const TraceGraph = ({ trace }) => {
  const nodesList = useMemo(() => {
    return trace.map(([transition, state], index) => ({
      id: `node-${index}`,
      data: {
        label: (
          <div className="p-2">
            <div className="font-semibold text-sm text-white">{transition}</div>
            <pre className="text-xs text-gray-200 font-mono whitespace-pre-wrap">
              {JSON.stringify(state, null, 1)}
            </pre>
          </div>
        ),
      },
      position: { x: index * 260, y: 0 },
      style: {
        background: "linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)",
        border: "2px solid #e0e7ff",
        borderRadius: 16,
        padding: 12,
        color: "#fff",
        width: 220,
        boxShadow: "0 6px 14px rgba(0,0,0,0.3)",
      },
    }));
  }, [trace]);

  const edgesList = useMemo(() => {
    return trace.slice(0, -1).map((_, index) => ({
      id: `e-${index}`,
      source: `node-${index}`,
      target: `node-${index + 1}`,
      type: "smoothstep",
      animated: true,
      style: { stroke: "#10b981", strokeWidth: 2 },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: "#10b981",
      },
    }));
  }, [trace]);

  const [nodes, , onNodesChange] = useNodesState(nodesList);
  const [edges, , onEdgesChange] = useEdgesState(edgesList);

  const onConnect = useCallback(
    (params) => addEdge({ ...params, animated: true }, edges),
    [edges]
  );

  return (
    <div className="h-[500px] w-full border rounded-2xl overflow-hidden mt-8 shadow-2xl bg-white dark:bg-zinc-900 transition-all duration-300">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        fitViewOptions={{ padding: 1 }}
      >
        <MiniMap
          nodeColor={() => "#4f46e5"}
          maskColor="rgba(255,255,255,0.6)"
        />
        <Controls position="bottom-left" />
        <Background color="#e5e7eb" gap={16} />
      </ReactFlow>
    </div>
  );
};

export default TraceGraph;

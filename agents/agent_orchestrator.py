"""
Agent 编排器
支持多 Agent 协作、任务分配和结果整合

【前端类比】
这就像前端的 "微前端架构" 或 "组件编排系统"
- AgentOrchestrator = 主应用/容器应用（类似 qiankun 的主应用）
- 各个 Agent = 子应用/微组件（类似微前端中的子应用）
- 任务路由 = 路由分发（类似 react-router 的路由匹配）
- 协作任务 = 组件间通信（类似 Redux 的状态共享）

例如：
```javascript
// 微前端主应用
const orchestrator = new MicroFrontendApp();
orchestrator.registerApp('coding', CodingApp);  // 注册子应用
orchestrator.registerApp('math', MathApp);

// 路由到特定子应用
orchestrator.navigateTo('/coding', task);

// 或者广播给所有子应用
orchestrator.broadcast(event);
```
"""

from typing import List, Dict, Any, Optional, Callable
from .base_agent import BaseAgent


class AgentOrchestrator:
    """
    Agent 编排器
    协调多个 Agent 协同完成任务
    
    【前端类比】
    就像微前端的主应用，或者 Redux Store 管理多个 reducer
    - 注册 Agent = 注册子应用/reducer
    - 路由任务 = dispatch action 到特定 reducer
    - 广播任务 = dispatch action 到所有 reducer
    - 协作任务 = 串联多个 middleware
    """
    
    def __init__(self, name: str = "Agent编排器"):
        """
        初始化编排器
        
        【前端类比】
        就像创建 Redux store 或微前端主应用
        ```javascript
        const store = createStore(rootReducer);
        // 或
        const mainApp = new MicroFrontendApp();
        ```
        """
        self.name = name
        self.agents: Dict[str, BaseAgent] = {}  # 注册的 Agent（类似已注册的子应用）
        self.agent_roles: Dict[str, str] = {}  # Agent 的角色描述（类似路由配置）
    
    def register_agent(self, agent: BaseAgent, role: str = None):
        """
        注册 Agent
        
        【前端类比】
        就像在微前端中注册子应用，或在 Redux 中注册 reducer
        
        类似：
        ```javascript
        // 微前端注册子应用
        registerMicroApps([
          { name: 'coding', entry: '//localhost:3001', container: '#coding' }
        ]);
        
        // Redux 注册 reducer
        combineReducers({
          coding: codingReducer,
          math: mathReducer
        });
        ```
        
        Args:
            agent: Agent 实例（类似子应用组件）
            role: Agent 的角色描述（类似路由路径或 reducer key）
        """
        agent_name = agent.name
        self.agents[agent_name] = agent
        self.agent_roles[agent_name] = role or "通用助手"
        print(f"已注册 Agent: {agent_name} (角色: {self.agent_roles[agent_name]})")
    
    def unregister_agent(self, agent_name: str):
        """注销 Agent"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            del self.agent_roles[agent_name]
            print(f"已注销 Agent: {agent_name}")
    
    def list_agents(self) -> List[Dict[str, str]]:
        """列出所有注册的 Agent"""
        return [
            {"name": name, "role": role}
            for name, role in self.agent_roles.items()
        ]
    
    def route_task(self, task: str, target_agent: str = None) -> str:
        """
        将任务路由到指定 Agent
        
        【前端类比】
        就像 React Router 的路由匹配，或 Redux 的 action dispatch
        
        类似：
        ```javascript
        // React Router 路由
        <Route path="/coding" element={<CodingAgent />} />
        
        // 或者 Redux dispatch
        dispatch({ type: 'CODING_TASK', payload: task });
        ```
        
        Args:
            task: 任务描述（类似用户输入或 action payload）
            target_agent: 目标 Agent 名称，None 则自动选择（类似路由路径）
        
        Returns:
            Agent 的响应（类似组件渲染结果或 reducer 返回的 state）
        """
        if target_agent:
            if target_agent not in self.agents:
                return f"错误: Agent '{target_agent}' 未注册"
            agent = self.agents[target_agent]
        else:
            # 简单策略：选择第一个 Agent（类似默认路由）
            if not self.agents:
                return "错误: 没有可用的 Agent"
            agent = list(self.agents.values())[0]
        
        print(f"任务路由到: {agent.name}")
        return agent.process(task)
    
    def broadcast_task(self, task: str) -> Dict[str, str]:
        """
        广播任务给所有 Agent
        
        【前端类比】
        就像 Redux 的 action 被所有 reducer 接收，或事件总线（Event Bus）
        
        类似：
        ```javascript
        // Redux: action 被所有 reducer 接收
        dispatch({ type: 'NOTIFY_ALL', payload: task });
        
        // 或 Event Bus
        eventBus.emit('task', task);  // 所有监听者都会收到
        
        // 或 WebSockets 广播
        ws.broadcast(message);  // 所有连接的客户端都收到
        ```
        
        Args:
            task: 任务描述
        
        Returns:
            所有 Agent 的响应（类似多个 reducer 返回的新 state）
        """
        results = {}
        for name, agent in self.agents.items():
            print(f"广播任务给: {name}")
            try:
                response = agent.process(task)
                results[name] = response
            except Exception as e:
                results[name] = f"错误: {str(e)}"
        
        return results
    
    def collaborative_task(
        self,
        task: str,
        agent_sequence: List[str],
        context_passing: bool = True
    ) -> Dict[str, Any]:
        """
        协作任务：按顺序让多个 Agent 处理
        
        Args:
            task: 初始任务
            agent_sequence: Agent 处理顺序
            context_passing: 是否传递上下文
        
        Returns:
            每个 Agent 的处理结果
        """
        results = {}
        current_context = task
        
        for agent_name in agent_sequence:
            if agent_name not in self.agents:
                results[agent_name] = f"错误: Agent '{agent_name}' 未注册"
                continue
            
            agent = self.agents[agent_name]
            print(f"执行步骤: {agent_name}")
            
            try:
                response = agent.process(current_context)
                results[agent_name] = response
                
                # 如果启用上下文传递，将当前结果作为下一个 Agent 的输入
                if context_passing:
                    current_context = f"前一步骤结果:\n{response}\n\n请继续处理。"
            
            except Exception as e:
                results[agent_name] = f"错误: {str(e)}"
                break
        
        return {
            "task": task,
            "sequence": agent_sequence,
            "results": results
        }
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """获取指定的 Agent"""
        return self.agents.get(agent_name)
    
    def reset_all(self):
        """重置所有 Agent"""
        for agent in self.agents.values():
            agent.reset()
        print("所有 Agent 已重置")


class TaskDecomposer:
    """
    任务分解器
    将复杂任务分解为子任务
    """
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
    
    def decompose(self, complex_task: str) -> List[Dict[str, str]]:
        """
        分解复杂任务
        
        Args:
            complex_task: 复杂任务描述
        
        Returns:
            子任务列表
        """
        # 这里可以使用 LLM 来智能分解任务
        # 简化实现：手动定义分解规则
        
        subtasks = []
        
        # 示例：如果任务包含多个关键词，进行分解
        if "分析" in complex_task and "报告" in complex_task:
            subtasks = [
                {"task": f"收集数据: {complex_task}", "agent_role": "数据收集"},
                {"task": f"分析数据: {complex_task}", "agent_role": "数据分析"},
                {"task": f"生成报告: {complex_task}", "agent_role": "报告生成"},
            ]
        else:
            subtasks = [
                {"task": complex_task, "agent_role": "通用"}
            ]
        
        return subtasks
    
    def execute_decomposed_task(
        self,
        complex_task: str,
        role_to_agent: Dict[str, str] = None
    ) -> List[Dict[str, str]]:
        """
        执行分解后的任务
        
        Args:
            complex_task: 复杂任务
            role_to_agent: 角色到 Agent 名称的映射
        
        Returns:
            各子任务的执行结果
        """
        subtasks = self.decompose(complex_task)
        results = []
        
        for subtask in subtasks:
            task_desc = subtask["task"]
            role = subtask["agent_role"]
            
            # 找到对应角色的 Agent
            target_agent = None
            if role_to_agent and role in role_to_agent:
                target_agent = role_to_agent[role]
            else:
                # 查找具有该角色的 Agent
                for agent_name, agent_role in self.orchestrator.agent_roles.items():
                    if role in agent_role or agent_role in role:
                        target_agent = agent_name
                        break
            
            if target_agent:
                result = self.orchestrator.route_task(task_desc, target_agent)
                results.append({
                    "subtask": task_desc,
                    "role": role,
                    "agent": target_agent,
                    "result": result
                })
            else:
                results.append({
                    "subtask": task_desc,
                    "role": role,
                    "agent": "未分配",
                    "result": "未找到合适的 Agent"
                })
        
        return results


# 便捷函数
def create_simple_orchestrator() -> AgentOrchestrator:
    """创建一个简单的 Agent 编排器"""
    return AgentOrchestrator(name="简单编排器")
